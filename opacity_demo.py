import sys

from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout, QStatusBar, QLabel, QProgressBar, QApplication, \
    QPushButton, QButtonGroup, QRadioButton, QFrame, QGraphicsOpacityEffect


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            #wd_test{
                background-color: red;
            }
            """)
        self.setup_ui()
        pass

    def setup_ui(self):
        # MainWindow的中心控件
        self.wd_central_widget = QWidget()
        self.setCentralWidget(self.wd_central_widget)
        self.vl_central_widget = QVBoxLayout(self.wd_central_widget)
        self.pb_test = QPushButton('TEST')
        self.pb_test.clicked.connect(self.test_clicked)
        # DEMO区域-start
        self.wd_test = QWidget()
        self.wd_test.setObjectName('wd_test')
        self.go_opacity_effect = QGraphicsOpacityEffect()
        self.wd_test.setGraphicsEffect(self.go_opacity_effect)
        self.go_opacity_effect.setOpacity(0.5)
        QTimer.singleShot(1000, self.change_opacity)
        # DEMO区域-end
        self.vl_central_widget.addWidget(self.pb_test)
        self.vl_central_widget.addWidget(self.wd_test, 1)
        self.vl_central_widget.addStretch(1)
        pass

    def change_opacity(self):
        self.go_opacity_effect.setOpacity(0.1)

    def test_clicked(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.showMaximized()
    sys.exit(app.exec_())
