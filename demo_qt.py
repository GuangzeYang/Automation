import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem


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
        self.lw_display_steps = QListWidget()
        item = QListWidgetItem("text")
        item.setCheckState(Qt.Unchecked)
        self.lw_display_steps.addItem(item)
        # DEMO-Stop
        self.vl_main.addWidget(self.pb_test)
        self.vl_main.addWidget(self.lw_display_steps)
        self.vl_main.addStretch(1)
        pass

    def test_click(self):
        print("Test Click")
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowTest()
    window.show()
    sys.exit(app.exec_())
    pass