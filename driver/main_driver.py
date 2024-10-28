import collections
import os
import time
from distutils.command.config import config
from importlib.resources import is_resource
from time import sleep

import yaml
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QDialog, QFileDialog
from loguru import logger
import json

from custom_widget.ui.independent_widget import FadeOutPrompt
from driver.wizard_driver import WizardDriver
from driver.operate_driver import OperateDriver
from driver.wizard_driver import OperateType, OperateAction
import threading
from driver.custom_tools import exception_is_executed_log

import configparser


class AutoDrive:

    def __init__(self):
        super().__init__()
        # 处理后的数据格式：[ 时间 ，操作，时间，操作......]，操作数据格式按被操作的对象划分。
        #   时间数据格式为{"type":OperateType.TIME, "time_interval":value}
        #   键盘操作数据格式{"type": OperateType.KEYBOARD, "object": key, "action": OperateAction.TAP}
        #   鼠标操作数据格式{"type": OperateType.MOUSE, "object": button, "action": "click", "x_pos": abs_x, "y_pos": abs_y}
        # 队列在头处pop时，性能高于list。list是动态分配内存，阈值时重新分配性能低，所以raw_step用队列，保证最小误差记录操作步骤。
        self.measure_step = []  # 保存所有定义的执行步骤

        self.actual_step = []  # 实际执行的步骤（用户在measure_step基础上进行操作/筛选后的步骤）
        self.user_config_path = "./static/config/user_config.ini"
        self.user_config = configparser.ConfigParser()  # 缓存最近操作的文件路径
        self.user_config.read(self.user_config_path)
        self.operate_driver = OperateDriver()
        self.wizard_driver = WizardDriver()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.operate_driver.open_file_action.triggered.connect(self.open_file)
        self.operate_driver.save_file_action.triggered.connect(self.save_file)

        self.operate_driver.pb_define_step.clicked.connect(self.define_step)
        self.operate_driver.pb_start_execution.clicked.connect(self.start_execution)
        self.operate_driver.pb_stop_execution.clicked.connect(self.stop_execution)
        self.operate_driver.pb_continue_execution.clicked.connect(self.continue_execution)

        self.wizard_driver.record_step_finished.connect(self.open_operate)
        self.wizard_driver.pause_executed.connect(self.open_operate)

    def show(self):
        self.operate_driver.show()
        pass

    def open_operate(self, raw_step: collections.deque = None):
        logger.info("切换至用户操作界面")
        self.operate_driver.show()
        self.wizard_driver.hide()
        self.operate_driver.activateWindow()
        self.operate_driver.setFocus()
        if raw_step:
            self.build_overall_step_queue(raw_step)
        self.wizard_driver.execute_paused_event.clear()
        pass

    def define_step(self):
        self.operate_driver.hide()
        self.wizard_driver.record_step_show()
        pass

    def start_execution(self):
        self.operate_driver.hide()
        # 处理实际执行的数据
        self.build_actual_step_queue()
        self.wizard_driver.loop_count = int(self.operate_driver.le_loop_count.text())
        self.wizard_driver.execute_step_show(self.actual_step)
        pass

    def stop_execution(self):
        pass

    def continue_execution(self):
        pass

    @exception_is_executed_log()
    def build_actual_step_queue(self):
        """构建实际的测量步骤"""
        self.actual_step.clear()
        is_reserved = True
        for i, step in enumerate(self.measure_step):
            if step.get("type") != OperateType.TIME:
                row = i/2
                item = self.operate_driver.lw_display_steps.item(row)
                is_reserved = True if item.checkState() else False
            self.actual_step.append(step) if is_reserved else ...

        pass

    @exception_is_executed_log()
    def build_overall_step_queue(self, raw_queue):
        if not raw_queue:
            return
        logger.debug(f"build_step_queue---raw_queue：{raw_queue}")
        self.measure_step.clear()  # 清空历史步骤
        self.measure_step.append({"type": OperateType.TIME, "interval_time": 3})
        # 处理第一个元素
        raw_step = raw_queue.popleft()
        pre_time_stamp = raw_step.pop("time_stamp")
        self.measure_step.append(raw_step)
        # 构造整体操作步骤
        while raw_queue:
            raw_step = raw_queue.popleft()
            # 后一个时间戳减去前一个时间戳
            interval_time = raw_step["time_stamp"] - pre_time_stamp
            # 插入步骤前的时间间隔
            self.measure_step.append({"type": OperateType.TIME, "interval_time": interval_time})
            # 更新前驱时间戳
            pre_time_stamp = raw_step.pop("time_stamp")
            # 插入步骤
            self.measure_step.append(raw_step)
        # 显示到step_view
        self.operate_driver.set_step_view_data(self.measure_step)
        pass

    @exception_is_executed_log()
    def save_file(self):
        recent_path = path if (path := self.user_config.get("user_config", "recent_path", fallback=None)) else "C:"
        file_path, _ = QFileDialog.getSaveFileName(self.operate_driver, "保存文件", recent_path, "Yaml(*.yaml *.yml)")
        if not file_path:
            logger.error("保存文件失败，未选择文件路径")
            return
        with open(file_path, "w", encoding="utf-8") as fp:
            temp_save_obj = dict()
            temp_save_obj["ui_info"] = self.operate_driver.get_ui_data()
            temp_save_obj["measure_step"] = self.measure_step
            yaml.safe_dump(temp_save_obj, fp)
        self.user_config.set("user_config", "recent_path", file_path)
        with open(self.user_config_path, 'w', encoding="utf-8") as fp:
            self.user_config.write(fp)
        pass

    @exception_is_executed_log()
    def open_file(self):
        recent_path = path if (path := self.user_config.get("user_config", "recent_path", fallback=None)) else "C:"
        file_path, _ = QFileDialog.getSaveFileName(self.operate_driver, "保存文件", recent_path, "Yaml(*.yaml *.yml)")
        if not os.path.isfile(file_path):
            logger.error("打开文件失败，未选择文件路径")
            return
        with open(file_path, "r", encoding="utf-8") as fp:
            all_data = yaml.safe_load(fp)
            self.measure_step = all_data["measure_step"]
            self.operate_driver.set_ui_data(all_data["ui_info"], self.measure_step)
            pass
        pass
