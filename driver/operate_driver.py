from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox

from loguru import logger
from custom_widget.ui.independent_widget import PromptCenterTop
from gui.operate_gui import OperateGui


class OperateDriver(OperateGui):

    def __init__(self):
        super().__init__()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.open_file_action.triggered.connect(self.open_file)
        self.save_file_action.triggered.connect(self.save_file)
        self.about_hisun_action.triggered.connect(self.about_hisun)


    def closeEvent(self, event):
        res = PromptCenterTop(QMessageBox.Information, "提示", "确定要退出吗？", [QMessageBox.Yes, QMessageBox.No]).exec()
        if res == QMessageBox.Yes:
            super().closeEvent(event)
        else:
            event.ignore()
        pass

    def open_file(self):
        pass

    def save_file(self):
        pass

    def about_hisun(self):
        url = QUrl("http://www.hisuntest.com/")
        QDesktopServices.openUrl(url)
        pass


