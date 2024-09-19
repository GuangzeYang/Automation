from PyQt5.QtWidgets import QMainWindow, QPushButton, QMenuBar, QMenu, QAction, QWidget, QVBoxLayout, QHBoxLayout


class OperateGui(QMainWindow):


    def __init__(self):
        super().__init__()
        with open("static/qss/operate.qss", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
        self.setup_ui()
        pass

    def setup_ui(self):
        self.resize(800, 600)
        self.setWindowTitle("Operate")

        self.menu_bar = QMenuBar()
        self.file_menu = QMenu("文件")
        self.open_file_action = QAction("Open Project")
        self.save_file_action = QAction("Save Project")
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.save_file_action)
        self.menu_bar.addMenu(self.file_menu)

        self.setMenuBar(self.menu_bar)

        self.wd_central = QWidget()
        self.setCentralWidget(self.wd_central)
        self.vl_central = QVBoxLayout(self.wd_central)

        self.hl_operate_buttons = QHBoxLayout()
        self.pb_start_execution = QPushButton("开始执行")
        self.pb_pause_execution = QPushButton("暂停执行")
        self.pb_continue_execution = QPushButton("继续执行")
        self.pb_stop_execution = QPushButton("停止执行")
        self.hl_operate_buttons.addWidget(self.pb_start_execution)
        self.hl_operate_buttons.addWidget(self.pb_pause_execution)
        self.hl_operate_buttons.addWidget(self.pb_continue_execution)
        self.hl_operate_buttons.addWidget(self.pb_stop_execution)

        self.vl_central.addLayout(self.hl_operate_buttons)
        pass