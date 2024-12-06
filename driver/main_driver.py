import collections
import os
import time
from pynput.keyboard import Listener as KListener

import yaml
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from loguru import logger
from qfluentwidgets import InfoBar, InfoBarPosition

from driver.auto_dataclass import OperateType, KeyboardAction, MouseAction
from driver.wizard_driver import WizardDriver
from driver.operate_driver import OperateDriver
from driver.custom_tools import exception_is_executed_log

import configparser


class AutoDrive:

    def __init__(self):
        super().__init__()
        # 处理后的数据格式：[ 时间 ，操作，时间，操作......]，操作数据格式按被操作的对象划分。
        # 队列在头处pop时，性能高于list。list是动态分配内存，阈值时重新分配性能低，所以raw_step用队列，保证最小误差记录操作步骤。
        self.measure_steps = []  # 保存所有定义的执行步骤

        self.actual_step = []  # 实际执行的步骤（用户在measure_steps基础上进行操作/筛选后的步骤）
        self.user_config_path = "./static/config/user_config.ini"
        self.operate_driver = OperateDriver()
        self.wizard_driver = WizardDriver()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.operate_driver.open_file_action.triggered.connect(self.open_file)
        self.operate_driver.save_file_action.triggered.connect(self.save_file)
        self.operate_driver.lw_display_steps.itemChanged.connect(self.update_step_status)
        self.operate_driver.pb_define_step.clicked.connect(lambda: self.define_execution())
        self.operate_driver.pb_start_execution.clicked.connect(lambda :self.start_execution())
        self.operate_driver.pb_debug_execution.clicked.connect(lambda: self.debug_execution())
        self.operate_driver.pb_continue_execution.clicked.connect(lambda: self.continue_execution())
        self.operate_driver.close_app_signal.connect(self.close_app)

        self.wizard_driver.define_step_finished.connect(self.define_execution_finish)
        self.wizard_driver.pause_executed.connect(self.pause_execution)
        self.wizard_driver.debug_stopped.connect(self.debug_execution_finish)
        self.wizard_driver.single_step_finished.connect(self.single_step_finish)

    def show(self):
        self.operate_driver.show()
        pass

    def close_app(self):
        self.wizard_driver.keyboard_listener.stop()
        self.wizard_driver.mouse_listener.stop()
        self.wizard_driver.close()
        pass

    def show_operate(self):
        logger.info("切换至用户操作界面")
        self.operate_driver.show()
        self.wizard_driver.hide()
        self.operate_driver.activateWindow()
        self.operate_driver.setFocus()
        pass

    @exception_is_executed_log("定义执行步骤")
    def define_execution(self):
        self.operate_driver.hide()
        self.wizard_driver.show()
        self.wizard_driver.define_step_entry()
        pass

    def define_execution_finish(self, raw_step):
        self.build_overall_step_queue(raw_step)
        self.show_operate()
        pass

    @exception_is_executed_log("开始自动操作")
    def start_execution(self):
        self.build_actual_step_queue()
        self.stop_executed_thread()
        self.wizard_driver.loop_count = int(self.operate_driver.le_loop_count.text())
        self.operate_driver.hide()
        self.wizard_driver.show()
        time.sleep(1)
        self.wizard_driver.execute_step_entry(self.actual_step)
        pass

    @exception_is_executed_log("暂停自动操作")
    def pause_execution(self):
        self.wizard_driver.execute_paused_event.clear()
        self.show_operate()
        pass

    @exception_is_executed_log("Debug模式")
    def debug_execution(self):
        self.stop_executed_thread()
        self.build_actual_step_queue()
        self.wizard_driver.central_hint.setText("Debug模式")
        self.wizard_driver.sub_hint.setText("（按Esc键返回操作界面，按Enter键执行下一步）")
        self.operate_driver.hide()
        self.wizard_driver.show()
        self.wizard_driver.debug_step_entry(self.actual_step)
        pass

    def debug_execution_finish(self):
        self.show_operate()
        pass

    @exception_is_executed_log("继续执行自动操作")
    def continue_execution(self):
        if not self.wizard_driver.execute_step_thread.is_alive():
            QMessageBox(QMessageBox.Warning, "警告", "当前尚未识别到正在执行的操作！").exec()
            return
        self.wizard_driver.execute_paused_event.set()
        self.wizard_driver.keyboard_listener = KListener(on_press=self.wizard_driver.listen_command_keyboard)
        self.wizard_driver.keyboard_listener.start()
        self.wizard_driver.show()
        self.operate_driver.hide()
        pass

    def stop_executed_thread(self):
        while any([self.wizard_driver.execute_step_thread.is_alive(),
                   self.wizard_driver.debug_threading.is_alive()]):
            self.wizard_driver.execute_paused_event.set()
            self.wizard_driver.debug_paused_event.set()
            self.wizard_driver.is_execute_finished = True
            time.sleep(0.1)
        self.wizard_driver.execute_paused_event.clear()
        self.wizard_driver.debug_paused_event.clear()
        pass

    def single_step_finish(self, index):
        item_text = self.operate_driver.lw_display_steps.item(index).text()
        InfoBar.success(
                title='执行成功！',
                content=item_text,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=1000,
                parent=self.wizard_driver
        )
        pass

    def update_step_status(self, item):
        """更新在列表中展示的step是否被选中的状态"""
        index = self.operate_driver.lw_display_steps.indexFromItem(item).row()
        if item.checkState() == Qt.Checked:
            self.measure_steps[index].is_checked = True
        elif item.checkState() == Qt.Unchecked:
            self.measure_steps[index].is_checked = False
        else:
            pass

    @exception_is_executed_log("构建实际执行的步骤序列")
    def build_actual_step_queue(self):
        """构建实际的测量步骤"""
        self.actual_step.clear()
        for step in self.measure_steps:
            item = self.operate_driver.lw_display_steps.item(step.list_item_id)
            is_reserved = True if item.checkState() else False
            self.actual_step.append(step) if is_reserved else None
        pass

    @exception_is_executed_log("构建整体的步骤序列")
    def build_overall_step_queue(self, raw_queue):
        """
        根据监听到的信息构建出全部操作
        :param raw_queue:
        :return:
        """
        if not raw_queue:
            return
        self.measure_steps.clear()  # 清空历史步骤
        self.operate_driver.lw_display_steps.clear()
        # 构造整体操作步骤
        list_item_id = 0
        while raw_queue:
            raw_step = raw_queue.popleft()
            post_time_stamp = raw_queue[0]["time_stamp"] if raw_queue else raw_step["time_stamp"]
            # 时间间隔
            interval_time = post_time_stamp - raw_step["time_stamp"]
            # 插入步骤
            if raw_step.get("type") == OperateType.KEYBOARD:
                action = KeyboardAction(raw_step["object"], raw_step["action"], interval_time, is_checked=True)
            elif raw_step.get("type") == OperateType.MOUSE and raw_step["object"] != "scroll":
                action = MouseAction(raw_step["action"], raw_step["x_pos"], raw_step["y_pos"],
                                     interval_time, True, raw_step["object"])
            elif raw_step.get("type") == OperateType.MOUSE:
                action = MouseAction(raw_step["action"], raw_step["x_pos"], raw_step["y_pos"], interval_time,True,
                                     raw_step["object"], raw_step["scroll_dx"], raw_step["scroll_dy"])

            else:
                logger.critical("未知的数据格式")
                raise Exception("解析操作失败")
            action.list_item_id = list_item_id
            self.measure_steps.append(action)
            list_item_id +=1
        # 显示到step_view
        self.operate_driver.set_step_view_data(self.measure_steps)
        pass

    @exception_is_executed_log("保存工程文件")
    def save_file(self, is_checked=False):
        user_config = configparser.ConfigParser()
        user_config.read(self.user_config_path)
        recent_path = path if (
                    (path := user_config.get("file_path", "recent_save_path", fallback=None)) and os.path.exists(
                path)) else "C:"
        file_path, _ = QFileDialog.getSaveFileName(self.operate_driver, "保存文件", recent_path, "Yaml(*.yaml *.yml)")
        if not file_path:
            logger.error("保存文件失败，未选择文件路径")
            return

        with open(self.user_config_path, 'w', encoding="utf-8") as fp:
            user_config.set("file_path", "recent_save_path", os.path.dirname(file_path))
            user_config.write(fp)
        with open(file_path, "w", encoding="utf-8") as fp:
            temp_save_obj = dict()
            temp_save_obj["ui_info"] = self.operate_driver.get_ui_data()
            temp_save_obj["measure_steps"] = self.measure_steps
            yaml.dump(temp_save_obj, fp)
        user_config.set("file_path", "recent_save_path", file_path)
        pass

    @exception_is_executed_log('打开工程文件')
    def open_file(self, is_checked=False):
        user_config = configparser.ConfigParser()
        user_config.read(self.user_config_path)
        recent_path = path if (
                    (path := user_config.get("file_path", "recent_open_path", fallback=None)) and os.path.exists(
                path)) else "C:"
        file_path, _ = QFileDialog.getOpenFileName(self.operate_driver, "保存文件", recent_path, "Yaml(*.yaml *.yml)")
        if not os.path.isfile(file_path):
            logger.error("打开文件失败，未选择文件路径")
            return
        with open(self.user_config_path, 'w', encoding="utf-8") as fp:
            user_config.set("file_path", "recent_open_path", os.path.dirname(file_path))
            user_config.write(fp)
        with open(file_path, "r", encoding="utf-8") as fp:
            all_data = yaml.load(fp, yaml.Loader)
            self.measure_steps = all_data["measure_steps"]
            self.operate_driver.lw_display_steps.clear()
            self.operate_driver.set_ui_data(all_data["ui_info"], self.measure_steps)
        pass
