import sys

from PyQt5.QtCore import QTimer, Qt, QEasingCurve, QVariantAnimation
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, \
    QGraphicsOpacityEffect, QLabel



class WindowTest(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(800, 800)
        self.setup_ui()
        pass

    def setup_ui(self):
        self.vl_main = QVBoxLayout(self)
        self.pb_test = QPushButton("Test")
        self.pb_test.clicked.connect(self.test_click)
        # DEMO-Start
        self.da_test = QDialog()
        self.da_test.setParent(self)
        # DEMO-Stop
        self.vl_main.addWidget(self.pb_test)
        self.vl_main.addStretch(1)
        pass

    def test_click(self):
        print("Test Click")
        self.da_test.show()
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowTest()
    window.show()
    sys.exit(app.exec_())
    pass