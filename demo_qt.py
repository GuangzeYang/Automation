import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton
from qfluentwidgets import InfoBarPosition, InfoBar


class WindowTest(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(800, 300)
        self.setup_ui()
        pass

    def setup_ui(self):
        self.vl_main = QVBoxLayout(self)
        self.pb_test = QPushButton("Test")
        self.pb_test.clicked.connect(self.test_click)
        # DEMO-Start
        # DEMO-Stop
        self.vl_main.addWidget(self.pb_test)
        self.vl_main.addStretch(1)
        pass

    def test_click(self):
        InfoBar.success(
                title='Lesson 4',
                content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=window
        )

        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowTest()
    window.show()
    sys.exit(app.exec_())
    pass