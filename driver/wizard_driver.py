import time

from PyQt5.QtCore import pyqtSignal
from loguru import logger
from gui.wizard_gui import WizardGui
from pynput.mouse import Listener as MListener
from pynput.mouse import Controller as MController
from pynput.keyboard import Listener as KListener, Key
from pynput.keyboard import Controller as KController
import collections
import pyautogui
from enum import Enum

# 同步时间
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

OperateType = Enum('OperateType', 'MOUSE KEYBOARD TIME')
OperateAction = Enum('OperateAction', 'CLICK SCROLL TAP MOVE DELAY')


class WizardDriver(WizardGui):
    record_step_finished = pyqtSignal(object)
    pause_executed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.raw_step = collections.deque(maxlen=1000)
        self.is_recording = False
        self.mouse_controller = MController()
        self.keyboard_controller = KController()
        pass

    def record_step_show(self):
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
        self.show()
        self.keyboard_listener = KListener(on_release=self.keyboard_on_release)
        self.keyboard_listener.start()
        self.execute_step(measure_step)
        pass

    def execute_step(self, measure_step:list):
        for step in measure_step:
            try:
                if step["type"] == OperateType.MOUSE:
                    self.execute_mouse(step)
                elif step["type"] == OperateType.KEYBOARD:
                    self.execute_keyboard(step)
                elif step["type"] == OperateType.TIME:
                    time.sleep(step["interval_time"])
                else:
                    pass
            except Exception as e:
                logger.error(e)
        self.central_hint.setText("操作步骤全部执行完毕")
        logger.success("操作步骤全部执行完成")
        pass

    def execute_mouse(self, step:dict):
        """
        :param step: {"type": OperateType.MOUSE, "object": button, "action": "click", "x_pos": abs_x, "y_pos": abs_y}
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
        :param step: {"type": OperateType.KEYBOARD, "object": key, "action": OperateAction.TAP}
        :return:
        """
        logger.debug(f"键盘操作：{step}")
        if step["action"] == OperateAction.TAP:
            self.keyboard_controller.tap(step["object"])
        pass

    def mouse_on_click(self, abs_x, abs_y, button, pressed):
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
        在键盘释放时加入步骤序列中

        键盘保存为步骤的格式说明：{{"time_stamp": 时间戳, "type": OperateType.KEYBOARD, "object": 被按的键, "action": 怎么按的}}
        :param key: 按下的键
        :return:
        """
        if key == Key.esc:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            # 触发信号
            if self.is_recording:
                self.record_step_finished.emit(self.raw_step)
            else:
                self.pause_executed.emit()
        elif self.is_recording:
            step = {"time_stamp": time.time(), "type": OperateType.KEYBOARD, "object": key, "action": OperateAction.TAP}
            self.raw_step.append(step)
        else:
            pass
        pass
