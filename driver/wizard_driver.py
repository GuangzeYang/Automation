import time

from PyQt5.QtCore import pyqtSignal
from loguru import logger
from gui.wizard_gui import WizardGui
from pynput.mouse import Listener as MListener
from pynput.mouse import Controller as MController
from pynput.keyboard import Listener as KListener, Key
from pynput.keyboard import Controller as KController
import keyboard
import collections
from driver.auto_dataclass import OperateType, OperateAction, MouseAction, KeyboardAction
import threading

# 同步时间
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

class WizardDriver(WizardGui):
    define_step_finished = pyqtSignal(object)
    pause_executed = pyqtSignal()
    debug_stopped = pyqtSignal()
    # 预留功能
    single_step_finished = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.raw_step = collections.deque()
        self.is_execute_finished = False
        self.loop_count = 1
        self.execute_step_thread = threading.Thread()
        self.debug_threading = threading.Thread()

        self.execute_paused_event = threading.Event()
        self.debug_paused_event = threading.Event()

        self.mouse_controller = MController()
        self.keyboard_controller = KController()
        self.keyboard_listener = KListener()
        self.mouse_listener = MListener()
        pass

    def define_step_entry(self):
        """定义用户操作 的入口"""
        self.central_hint.setText("键入 ESC 键保存&退出当前操作界面")
        self.sub_hint.setText("（键盘与鼠标交替操作，不支持热键，不支持拖拽）")
        # 清空原始步骤队列，防止存在脏数据
        self.raw_step.clear()
        # 创建监听器。他妈的，这东西还不让重复使用！垃圾库！
        self.keyboard_listener = KListener(on_release=self.define_step_keyboard)
        self.mouse_listener = MListener(on_click=self.define_step_mouse_click, on_scroll=self.define_step_mouse_on_scroll)
        logger.info("开始监听鼠标与键盘hook操作")
        self.mouse_listener.start()
        self.keyboard_listener.start()
        pass

    def define_step_keyboard(self, key):
        """监听用户执行的键盘操作"""
        if key == Key.esc:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
            self.define_step_finished.emit(self.raw_step)
        else:
            step = {"time_stamp": time.time(), "type": OperateType.KEYBOARD, "object": key, "action": OperateAction.TAP}
            self.raw_step.append(step)
        pass

    def define_step_mouse_click(self, abs_x, abs_y, button, pressed):
        """监听用户执行的鼠标操作，以按下为准"""
        if pressed:
            step = {"time_stamp": time.time(), "type": OperateType.MOUSE, "object": button, "action": OperateAction.CLICK,
                    "x_pos": abs_x, "y_pos": abs_y}
            self.raw_step.append(step)
        pass

    def define_step_mouse_on_scroll(self, abs_x, abs_y, dx, dy):
        """监听用户执行的鼠标操作，以按下为准"""
        step = {"time_stamp": time.time(), "type": OperateType.MOUSE, "object": "scroll", "action": OperateAction.SCROLL,
                "x_pos": abs_x, "y_pos": abs_y, "scroll_dx": dx, "scroll_dy": dy}
        self.raw_step.append(step)
        pass

    def debug_step_entry(self, measure_step: list):
        self.is_execute_finished = False
        hook_enter = keyboard.on_press_key("enter",self.debug_next_step, suppress=True)
        hook_esc = keyboard.on_press_key("esc",lambda event: self.debug_finish(event, hook_enter, hook_esc),
                                         suppress=True)
        self.debug_threading = threading.Thread(target=self.debug_step, args=(measure_step,), name="debug_threading")
        self.debug_threading.daemon = True
        self.debug_threading.start()
        pass

    def debug_step(self, measure_step:list):
        for index, step in enumerate(measure_step):
            self.debug_paused_event.clear()
            self.debug_paused_event.wait()
            if self.is_execute_finished:
                return
            try:
                if isinstance(step, MouseAction):
                    self.execute_mouse(step, is_debug=True)
                elif isinstance(step, KeyboardAction):
                    self.execute_keyboard(step, is_debug=True)
                else:
                    pass
                self.single_step_finished.emit(index)
            except Exception as e:
                logger.error(e)

    def debug_next_step(self, event):
        if not self.debug_threading.is_alive():
            self.central_hint.setText("Debug模式")
            self.sub_hint.setText("（当前所有步骤全部执行完毕！esc可返回操作界面!）")
            pass
        elif not self.debug_paused_event.is_set():
            self.debug_paused_event.set()
        else:
            print("Debug模式点击太快了")

    def debug_finish(self, event, *args):
        for hook in args:
            keyboard.unhook(hook)
        self.is_execute_finished = True
        self.debug_stopped.emit()
        pass

    def execute_step_entry(self, measure_step: list):
        self.is_execute_finished = False
        self.central_hint.setText("正在执行操作步骤")
        self.sub_hint.setText("（尽量不要操作，可以按Esc键暂停执行）")
        self.execute_paused_event.set()

        self.keyboard_listener = KListener(on_release=self.listen_command_keyboard)
        self.keyboard_listener.start()
        self.execute_step_thread = threading.Thread(target=self.execute_step, args=(measure_step,), name="execute_threading")
        self.execute_step_thread.daemon = True
        self.execute_step_thread.start()
        pass

    def execute_step(self, measure_step:list):
        """执行保存的步骤"""
        for i in range(self.loop_count):
            for index, step in enumerate(measure_step):
                self.execute_paused_event.wait()
                if self.is_execute_finished:
                    return
                try:
                    if isinstance(step, MouseAction):
                        self.execute_mouse(step)
                    elif isinstance(step, KeyboardAction):
                        self.execute_keyboard(step)
                    else:
                        pass
                    self.single_step_finished.emit(index)
                except Exception as e:
                    logger.error(e)
        self.central_hint.setText("操作步骤全部执行完毕")
        self.sub_hint.setText("（可以按Esc键返回用户操作界面）")
        logger.success("操作步骤全部执行完成")
        pass

    def execute_mouse(self, step:MouseAction, is_debug:bool=False):
        """
        执行生成的步骤中鼠标部分
        :param step:
        :param is_debug: 当前是否时debug模式执行操作
        :return:
        """
        logger.debug(f"鼠标操作：{step}")
        if step.action == OperateAction.CLICK:
            self.mouse_controller.position = (step.x_pos, step.y_pos)
            self.mouse_controller.click(step.button)
        elif step.action == OperateAction.SCROLL:
            self.mouse_controller.position = (step.x_pos, step.y_pos)
            self.mouse_controller.scroll(0, 0)
        else:
            pass
        if not is_debug:
            time.sleep(step.delay)

    def execute_keyboard(self, step:KeyboardAction, is_debug:bool=False):
        """
        执行生成步骤中键盘部分
        :param is_debug:
        :param step:
        :return:
        """
        logger.debug(f"键盘操作：{step}")
        if step.action == OperateAction.TAP:
            self.keyboard_controller.tap(step.key)
        if not is_debug:
            time.sleep(step.delay)
        pass

    def listen_command_keyboard(self, key):
        if key == Key.esc:
            self.pause_executed.emit()
            self.keyboard_listener.stop()
        else:
            pass
        pass
