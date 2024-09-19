
import sys

from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout, QStatusBar, QLabel, QProgressBar, QApplication, \
    QPushButton, QButtonGroup, QRadioButton, QFrame, QMessageBox, QDialog


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('qt_nature')
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(500, 500)
        self.prompt_dialog = QDialog()
        self.prompt_dialog.setWindowTitle('提示')
        self.prompt_dialog.setAccessibleName('prompt_dialog')
        self.btn_ok = QPushButton('确定', self.prompt_dialog)
        self.btn_ok.setAccessibleName('btn_ok')
        # self.message_dialog = QMessageBox.information(self, '说明', f"点击成功:{self.frameGeometry()}", QMessageBox.Yes)
        self.setup_ui()
        pass

    # 初始化时的控件显示
    def setup_ui(self):
        # MainWindow的中心控件
        self.wd_central_widget = QWidget()
        # self.wd_central_widget.setStyleSheet('background-color: cyan')
        self.setCentralWidget(self.wd_central_widget)
        # DEMO区域-start
        self.pb_test = QPushButton('测试按钮')
        self.pb_test.setAccessibleName('pb_test')
        # self.pb_test.setObjectName('btn_test')
        self.pb_test.setParent(self.wd_central_widget)
        self.pb_test.move(20, 20)
        self.pb_test.setFixedSize(100, 100)
        self.pb_test.clicked.connect(self.test_click)
        # DEMO区域-end
        # self.vl_central_widget.addWidget(self.pb_test)
        # self.vl_central_widget.addStretch(1)
        pass

    def test_click(self):
        self.prompt_dialog.show()
        ...




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    print(window.size())
    print(window.geometry())
    print(window.frameGeometry())
    sys.exit(app.exec_())

