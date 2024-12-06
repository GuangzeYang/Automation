from PyQt5.QtCore import QUrl, pyqtSignal, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem

from loguru import logger
from pynput.mouse import Button

from custom_widget.ui.independent_widget import PromptCenterTop
from driver.auto_dataclass import KeyboardAction, MouseAction
from gui.operate_gui import OperateGui
from driver.auto_dataclass import OperateType, OperateAction
from typing import Union


class OperateDriver(OperateGui):
    close_app_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.about_hisun_action.triggered.connect(self.about_hisun)

    def closeEvent(self, event):
        res = PromptCenterTop(QMessageBox.Information, "提示", "确定要退出吗？", [QMessageBox.Yes, QMessageBox.No]).exec()
        if res == QMessageBox.Yes:
            self.close_app_signal.emit()
            super().closeEvent(event)
        else:
            event.ignore()
        pass

    def about_hisun(self):
        url = QUrl("http://www.hisuntest.com/")
        QDesktopServices.openUrl(url)
        pass

    def get_ui_data(self):
        loop_count = self.le_loop_count.text()

        ui_info = dict()
        ui_info["loop_count"] = int(loop_count)
        return ui_info

    def set_ui_data(self, ui_info, step_info):
        self.le_loop_count.setText(ui_info.get("loop_count", None).__str__())
        self.set_step_view_data(step_info)
        pass

    def set_step_view_data(self, measure_steps):
        """批量插入数据"""
        for step in measure_steps:
            self.add_step_item(step)
        pass

    def add_step_item(self, step_info:Union[KeyboardAction, MouseAction]):
        """
        向步骤列表中添加单个定义的步骤信息
        :param step_info:
        :return:
        """
        if isinstance(step_info, KeyboardAction):
            text = f"键盘--{step_info.key}--{'TAB' if step_info.action == OperateAction.TAP else None}"
            pass
        elif isinstance(step_info, MouseAction):
            action = "单击" if step_info.action == OperateAction.CLICK else "滚动"
            postfix_info = ""
            if step_info.button == Button.left:
                button = "左键"
            elif step_info.button == Button.right:
                button = "右键"
            elif step_info.button == Button.middle:
                button = "中键"
            else:
                button = "滚轮"
                postfix_info = f"--dx({step_info.scroll_dx})--dy({step_info.scroll_dy})"
            text = f"鼠标--{button}--{action}--pos{(step_info.x_pos, step_info.y_pos)}{postfix_info}"
            pass
        else:
            return
        item = QListWidgetItem(text)
        item.setCheckState(Qt.Checked) if step_info.is_checked else item.setCheckState(Qt.Unchecked)
        self.lw_display_steps.addItem(item)
        pass



