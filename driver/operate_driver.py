from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox

from custom_widget.ui.independent_widget import PromptCenterTop
from gui.operate_gui import OperateGui


class OperateDriver(OperateGui):
    open_wizard = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.open_file_action.triggered.connect(self.open_file)
        self.save_file_action.triggered.connect(self.save_file)
        self.about_hisun_action.triggered.connect(self.about_hisun)
        self.pb_start_execution.clicked.connect(self.start_execution)
        self.pb_stop_execution.clicked.connect(self.stop_execution)
        self.pb_continue_execution.clicked.connect(self.continue_execution)
        self.pb_pause_execution.clicked.connect(self.pause_execution)

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
        # 借用显示向导界面
        self.open_wizard.emit()
        pass

    def about_hisun(self):
        url = QUrl("http://www.hisuntest.com/")
        QDesktopServices.openUrl(url)
        pass

    def start_execution(self):
        pass

    def stop_execution(self):
        pass

    def pause_execution(self):
        pass

    def continue_execution(self):
        pass
