import collections

from loguru import logger
import json
from driver.wizard_driver import WizardDriver
from driver.operate_driver import OperateDriver
from driver.wizard_driver import OperateType, OperateAction
import threading


class AutoDrive:

    def __init__(self):
        super().__init__()
        # 处理后的数据格式：[ 时间 ，操作，时间，操作......]，操作数据格式按被操作的对象划分，时间数据格式为{"type":TIME, "time_interval":value}
        # 队列在头处pop时，性能高于list。list是动态分配内存，阈值时重新分配性能低，所以raw_step用队列，保证最小误差记录操作步骤。
        self.measure_step = []
        self.operate_driver = OperateDriver()
        self.wizard_driver = WizardDriver()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
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
            self.build_step_queue(raw_step)
        pass

    def define_step(self):
        self.operate_driver.hide()
        self.wizard_driver.record_step_show()
        pass

    def start_execution(self):
        self.operate_driver.hide()
        self.wizard_driver.execute_step_show(self.measure_step)
        pass

    def stop_execution(self):
        pass

    def continue_execution(self):
        pass

    def build_step_queue(self, raw_queue):
        if not raw_queue:
            return
        logger.debug(f"build_step_queue---raw_queue：{raw_queue}")
        logger.info("开始构建测试步骤......")
        self.measure_step.append({"type": OperateType.TIME, "interval_time": 3})
        # 处理第一个元素
        raw_step = raw_queue.popleft()
        pre_time_stamp = raw_step.pop("time_stamp")
        self.measure_step.append(raw_step)
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
        logger.success(f"操作步骤已成功生成")
        pass
