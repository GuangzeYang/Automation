import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout


class WizardGui(QWidget):

    def __init__(self):
        super().__init__()
        with open("./static/qss/wizard.qss", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
        # self.screen_geometry = QDesktopWidget().availableGeometry()
        self.screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.setup_ui()
        pass

    def setup_ui(self):
        # 设置窗口状态
        self.move(0, 0)
        self.resize(self.screen_geometry.width(), 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowTransparentForInput | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.7)

        self.vl_central = QVBoxLayout(self)

        self.hl_quit_center = QHBoxLayout()
        self.quit_hint = QLabel("键入 ESC 键退出定义操作界面")
        self.hl_quit_center.addStretch(1)
        self.hl_quit_center.addWidget(self.quit_hint)
        self.hl_quit_center.addStretch(1)

        self.vl_central.addLayout(self.hl_quit_center)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wizard = WizardGui()
    wizard.show()
    sys.exit(app.exec_())
    pass