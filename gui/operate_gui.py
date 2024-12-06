
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QWidget, QVBoxLayout, QHBoxLayout, QFrame, \
    QFormLayout, QLabel, QListWidget, QPushButton

from custom_widget.ui.button import HoverLargeButton
from custom_widget.ui.independent_widget import VSeparateLine
from custom_widget.ui.text_widget import LineEditVerify
from qfluentwidgets import ListWidget, LineEdit, RoundMenu, FluentIcon, Action


class OperateGui(QMainWindow):


    def __init__(self):
        super().__init__()
        with open("static/qss/operate.qss", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
        self.setup_ui()
        pass

    def setup_ui(self):
        self.resize(1000, 800)
        self.setWindowTitle("Operate")

        self.menu_bar = QMenuBar()

        self.file_menu = QMenu("文件")
        self.open_file_action = Action(FluentIcon.FOLDER, "Open Project")
        self.save_file_action = Action(FluentIcon.SAVE, "Save Project")
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.save_file_action)

        self.about_menu = QMenu("关于")
        self.about_hisun_action = Action(FluentIcon.LINK, "Hisun Test")
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
        self.pb_define_step = HoverLargeButton("定义操作")
        self.pb_start_execution = HoverLargeButton("开始执行")
        self.pb_continue_execution = HoverLargeButton("继续执行")
        self.pb_debug_execution = HoverLargeButton("调试执行")

        self.pb_define_step.setObjectName("define_step")
        self.pb_start_execution.setObjectName("start_execution")
        self.pb_continue_execution.setObjectName("continue_execution")
        self.pb_debug_execution.setObjectName("stop_execution")

        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_define_step,2)
        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_start_execution,2)
        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_continue_execution,2)
        self.hl_operate_buttons.addStretch(1)
        self.hl_operate_buttons.addWidget(self.pb_debug_execution,2)
        self.hl_operate_buttons.addStretch(1)

        # 添加按钮区与操作区的水平分割线
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.HLine)  # 设置为水平线
        self.h_line.setFrameShadow(QFrame.Sunken)  # 设置阴影样式

        self.hl_operate_info = QHBoxLayout()

        # 收集用户输入信息区域
        self.wd_gather_info = QWidget()
        self.fl_gather_info = QFormLayout(self.wd_gather_info)
        self.fl_gather_info.setVerticalSpacing(10)
        self.fl_gather_info.setHorizontalSpacing(20)

        # 获取循环次数
        self.lb_loop_count = QLabel("循环次数:")
        self.le_loop_count = LineEdit()
        self.le_loop_count.setText("1")
        self.le_loop_count.setValidator(QIntValidator(1, 100))

        # 获取打开项目文件的路径
        self.hl_open_project = QHBoxLayout()
        self.le_open_project_path = LineEditVerify()
        self.le_open_project_path.setPlaceholderText("例如：C:/hisun/test/666.yaml")
        self.pb_open_project = QPushButton("选择")
        self.pb_open_project.setObjectName("pb_open_project")
        self.hl_open_project.addWidget(self.le_open_project_path,7)
        self.hl_open_project.addStretch(1)
        self.hl_open_project.addWidget(self.pb_open_project,2)

        self.fl_gather_info.addRow(self.lb_loop_count, self.le_loop_count)
        # self.fl_gather_info.addRow("打开项目文件：", self.hl_open_project)

        # 划分左右两部分的垂直分割线
        self.vertical_separator = VSeparateLine()

        # 显示当前定义的步骤
        self.wd_operate_steps = QWidget()
        self.vl_operate_steps = QVBoxLayout(self.wd_operate_steps)

        self.fm_display_frame = QFrame()
        self.fm_display_frame.setObjectName("fm_display_frame")
        self.fm_display_frame.setFrameShape(QFrame.Box)
        self.hl_frame = QHBoxLayout(self.fm_display_frame)
        self.lw_display_steps = ListWidget()
        self.hl_frame.addWidget(self.lw_display_steps)

        self.hl_steps_btns = QHBoxLayout()  # TODO 添加有关对步骤操作的按钮
        self.vl_operate_steps.addWidget(self.fm_display_frame, 3)
        self.vl_operate_steps.addStretch(1)

        self.hl_operate_info.addWidget(self.wd_gather_info,1)
        self.hl_operate_info.addWidget(self.vertical_separator)
        self.hl_operate_info.addWidget(self.wd_operate_steps,1)

        # 添加底部水平分割线，要不太丑了
        self.h_bottom_line = QFrame()
        self.h_bottom_line.setFrameShape(QFrame.HLine)  # 设置为水平线
        self.h_bottom_line.setFrameShadow(QFrame.Sunken)  # 设置阴影样式

        # 用户设置部分
        self.vl_central.addWidget(self.wd_operate_buttons, 1)
        self.vl_central.addWidget(self.h_line)
        self.vl_central.addLayout(self.hl_operate_info,6)
        self.vl_central.addWidget(self.h_bottom_line)
        self.vl_central.addStretch(1)
        pass