import time

from PyQt5.QtCore import pyqtSignal
from loguru import logger
from gui.wizard_gui import WizardGui
from pynput.mouse import Listener as MListener
from pynput.mouse import Controller as MController
from pynput.keyboard import Listener as KListener, Key
from pynput.keyboard import Controller as KController
import collections
from driver.custom_enum import OperateType, OperateAction
import threading

# 同步时间
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

class WizardDriver(WizardGui):
    record_step_finished = pyqtSignal(object)
    pause_executed = pyqtSignal()
    single_step_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.raw_step = collections.deque(maxlen=1000)
        self.is_recording = False
        self.loop_count = 1
        self.execute_paused_event = threading.Event()
        self.mouse_controller = MController()
        self.keyboard_controller = KController()
        pass

    def record_step_show(self):
        """记录 用户操作 的入口"""
        logger.info("进入步骤定义 向导界面")
        # 设置提示信息内容
        self.central_hint.setText("键入 ESC 键保存&退出当前操作界面")
        self.sub_hint.setText("（键盘与鼠标交替操作，不支持热键，不支持拖拽）")
        self.show()
        # 清空原始步骤队列，防止存在脏数据
        self.raw_step.clear()
        # 创建监听器。他妈的，这东西还不让重复使用！垃圾库！
        self.keyboard_listener = KListener(on_release=self.keyboard_on_release)
        self.mouse_listener = MListener(on_click=self.mouse_on_click, on_scroll=self.mouse_on_scroll)
        self.is_recording = True
        logger.info("开始监听鼠标与键盘操作")
        self.mouse_listener.start()
        self.keyboard_listener.start()
        pass

    def execute_step_show(self, measure_step: list):
        self.central_hint.setText("正在执行操作步骤")
        self.sub_hint.setText("（尽量不要操作，可以按Esc键暂停执行）")
        self.is_recording = False
        self.show()
        self.keyboard_listener = KListener(on_release=self.keyboard_on_release)
        self.keyboard_listener.start()
        self.execute_step_thread = threading.Thread(target=self.execute_step, args=(measure_step,))
        self.execute_step_thread.daemon = True
        self.execute_step_thread.start()
        pass

    def debug_step_show(self, measure_step: list):
        self.central_hint.setText("Debug模式")
        self.sub_hint.setText("（按Esc键返回，按Alt键执行下一步）")
        self.is_recording = False
        self.show()
        self.keyboard_listener = KListener(on_release=self.keyboard_on_release)
        self.keyboard_listener.start()
        self.execute_step_thread = threading.Thread(target=self.execute_step, args=(measure_step,))
        self.execute_step_thread.daemon = True
        self.execute_step_thread.start()
        pass

    def execute_step(self, measure_step:list):
        """执行保存的步骤"""
        self.execute_paused_event.set()
        for i in range(self.loop_count):
            for step in measure_step:
                self.execute_paused_event.wait()
                try:
                    if step["type"] == OperateType.MOUSE:
                        self.execute_mouse(step)
                        self.single_step_finished.emit()
                    elif step["type"] == OperateType.KEYBOARD:
                        self.execute_keyboard(step)
                        self.single_step_finished.emit()
                    elif step["type"] == OperateType.TIME:
                        time.sleep(step["interval_time"])
                    else:
                        pass
                except Exception as e:
                    logger.error(e)
        self.central_hint.setText("操作步骤全部执行完毕")
        self.sub_hint.setText("（可以按Esc键返回用户操作界面）")
        logger.success("操作步骤全部执行完成")
        pass

    def execute_mouse(self, step:dict):
        """
        执行生成的步骤中鼠标部分
        :param step: {"type": OperateType.MOUSE, "object": button, "action": "OperateAction.CLICK", "x_pos": abs_x, "y_pos": abs_y}
        :return:
        """
        logger.debug(f"鼠标操作：{step}")
        if step["action"] == OperateAction.CLICK:
            self.mouse_controller.position = (step["x_pos"], step["y_pos"])
            self.mouse_controller.click(step["object"])
        elif step["action"] == OperateAction.SCROLL:
            self.mouse_controller.position = (step["x_pos"], step["y_pos"])
            self.mouse_controller.scroll(0, step["object"])
        else:
            pass
        pass

    def execute_keyboard(self, step:dict):
        """
        执行生成步骤中键盘部分
        :param step: {"type": OperateType.KEYBOARD, "object": key, "action": OperateAction.TAP}
        :return:
        """
        logger.debug(f"键盘操作：{step}")
        if step["action"] == OperateAction.TAP:
            self.keyboard_controller.tap(step["object"])
        pass

    def mouse_on_click(self, abs_x, abs_y, button, pressed):
        """监听记录鼠标事件，以按下为准"""
        if pressed:
            step = {"time_stamp": time.time(), "type": OperateType.MOUSE, "object": button, "action": OperateAction.CLICK, "x_pos": abs_x, "y_pos": abs_y}
            self.raw_step.append(step)
        pass

    def mouse_on_scroll(self, abs_x, abs_y, dx, dy):
        # step = {"time_stamp": time.time(), "type": OperateType.MOUSE, "object": "scroll", "action": "scroll", "x_pos": abs_x, "y_pos": abs_y}
        # self.raw_step.append(step)
        pass

    def keyboard_on_release(self, key):
        """
        这是一个pynput监听事件时的线程，所以通信使用信号
        监听记录键盘事件：is_recording为真时，在键盘释放时加入步骤序列中。ESC直接退出向导界面

        键盘保存为步骤的格式说明：{{"time_stamp": 时间戳, "type": OperateType.KEYBOARD, "object": 被按的键, "action": 怎么按的}}
        :param key: 按下的键
        :return:
        """
        if key == Key.esc and self.is_recording:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
            self.record_step_finished.emit(self.raw_step)
            self.is_recording = False
        elif key == Key.esc:
            self.pause_executed.emit()

        elif self.is_recording:
            step = {"time_stamp": time.time(), "type": OperateType.KEYBOARD, "object": key, "action": OperateAction.TAP}
            self.raw_step.append(step)
        else:
            pass
        pass
