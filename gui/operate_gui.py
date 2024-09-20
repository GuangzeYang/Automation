from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QWidget, QVBoxLayout, QHBoxLayout, QFrame

from custom_widget.ui.button import HoverLargeButton


class OperateGui(QMainWindow):


    def __init__(self):
        super().__init__()
        with open("static/qss/operate.qss", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
        self.setup_ui()
        pass

    def setup_ui(self):
        self.resize(1200, 1000)
        self.setWindowTitle("Operate")

        self.menu_bar = QMenuBar()

        self.file_menu = QMenu("文件")
        self.open_file_action = QAction("Open Project")
        self.save_file_action = QAction("Save Project")
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.save_file_action)

        self.about_menu = QMenu("关于")
        self.about_hisun_action = QAction("Hisun Test")
        self.about_menu.addAction(self.about_hisun_action)

        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.about_menu)

        # 主界面设置菜单栏
        self.setMenuBar(self.menu_bar)

        self.wd_central = QWidget()
        self.setCentralWidget(self.wd_central)
        self.vl_central = QVBoxLayout(self.wd_central)

        self.wd_operate_buttons = QWidget()
        self.hl_operate_buttons = QHBoxLayout(self.wd_operate_buttons)
        # 设置上边距
        self.hl_operate_buttons.setContentsMargins(0, 10, 0, 0)
        self.pb_start_execution = HoverLargeButton("开始执行")
        self.pb_pause_execution = HoverLargeButton("暂停执行")
        self.pb_continue_execution = HoverLargeButton("继续执行")
        self.pb_stop_execution = HoverLargeButton("停止执行")

        self.pb_start_execution.setObjectName("start_execution")
        self.pb_pause_execution.setObjectName("pause_execution")
        self.pb_continue_execution.setObjectName("continue_execution")
        self.pb_stop_execution.setObjectName("stop_execution")

        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_start_execution,2)
        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_pause_execution,2)
        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_continue_execution,2)
        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_stop_execution,2)
        self.hl_operate_buttons.addStretch(1)

        # 添加水平分割线
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.HLine)  # 设置为水平线
        self.h_line.setFrameShadow(QFrame.Sunken)  # 设置阴影样式

        # 用户设置部分

        self.vl_central.addWidget(self.wd_operate_buttons, 1)
        self.vl_central.addWidget(self.h_line)
        self.vl_central.addStretch(7)
        pass