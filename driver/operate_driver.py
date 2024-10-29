from PyQt5.QtCore import QUrl, pyqtSignal, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem

from loguru import logger
from pynput.mouse import Button

from custom_widget.ui.independent_widget import PromptCenterTop
from gui.operate_gui import OperateGui
from driver.custom_enum import OperateType, OperateAction


class OperateDriver(OperateGui):

    def __init__(self):
        super().__init__()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.about_hisun_action.triggered.connect(self.about_hisun)

    def closeEvent(self, event):
        res = PromptCenterTop(QMessageBox.Information, "提示", "确定要退出吗？", [QMessageBox.Yes, QMessageBox.No]).exec()
        if res == QMessageBox.Yes:
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

    def set_step_view_data(self, step_info):
        """批量插入数据"""
        for step in step_info:
            self.add_step_item(step)
        pass

    def add_step_item(self, step_info:dict):
        """
        向步骤列表中添加单个定义的步骤信息
        :param step_info:
        #   时间数据格式为{"type":TIME, "time_interval":value}
        #   键盘操作数据格式{"type": OperateType.KEYBOARD, "object": key, "action": OperateAction.TAP, "is_checked":bool }
        #   鼠标操作数据格式{"type": OperateType.MOUSE, "object": button, "action": "OperateAction.CLICK", "x_pos": abs_x, "y_pos": abs_y, "is_checked":bool }
        :return:
        """
        if step_info["type"] == OperateType.TIME:
            return
        elif step_info["type"] == OperateType.KEYBOARD:
            text = f"键盘--{step_info.get('object')}--{'TAB' if step_info.get('action') == OperateAction.TAP else None}"
            pass
        elif step_info["type"] == OperateType.MOUSE:
            action = "单击" if step_info.get("action") == OperateAction.CLICK else None
            if step_info.get('object') == Button.left:
                button = "左键"
            elif step_info.get('object') == Button.right:
                button = "右键"
            else:
                button = None
            text = f"鼠标--{button}--{action}--pos{(step_info.get('x_pos'), step_info.get('y_pos'))}"
            pass
        else:
            return
        item = QListWidgetItem(text)
        item.setCheckState(Qt.Checked) if step_info["is_checked"] else item.setCheckState(Qt.Unchecked)
        self.lw_display_steps.addItem(item)
        pass



