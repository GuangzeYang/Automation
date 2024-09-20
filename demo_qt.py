import sys

from PyQt5.QtCore import Qt, QTimer, QRect, pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout, QStatusBar, QLabel, QProgressBar, QApplication, \
    QPushButton, QButtonGroup, QRadioButton, QFrame, QHBoxLayout, QLayout, QSizePolicy

import sys
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty, QParallelAnimationGroup, QRect
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtGui import QFont


class HoverLargeButton(QPushButton):
    """悬浮变大按钮"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.__zoom_factor = 2
        self.__zoom_factor_rect = 4
        self.__zoom_factor_font = 1.5
        self.__zoom_duration = 80
        self.__geometry_before_zoom = self.geometry()
        self.__font_size_before_zoom = self.font().pointSizeF()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)



        self.zoom_in_geometry = QPropertyAnimation(self, b'cus_geometry')
        self.zoom_in_font = QPropertyAnimation(self, b'font_size')
        self.zoom_in_geometry.setDuration(self.__zoom_duration)
        self.zoom_in_font.setDuration(self.__zoom_duration)

        self.zoom_out_geometry = QPropertyAnimation(self, b'geometry')
        self.zoom_out_font = QPropertyAnimation(self, b'font_size')
        self.zoom_out_geometry.setDuration(self.__zoom_duration)
        self.zoom_out_font.setDuration(self.__zoom_duration)

        self.__is_zoom_in_finished = True
        self.zoom_in_group = QParallelAnimationGroup()
        # self.zoom_in_group.finished.connect(self.zoom_in_finish)
        self.zoom_in_group.addAnimation(self.zoom_in_geometry)
        self.zoom_in_group.addAnimation(self.zoom_in_font)

        self.__is_zoom_out_finished = True
        self.zoom_out_group = QParallelAnimationGroup()
        self.zoom_out_group.finished.connect(self.zoom_out_finish)
        self.zoom_out_group.addAnimation(self.zoom_out_geometry)
        self.zoom_out_group.addAnimation(self.zoom_out_font)
        pass

    def enterEvent(self, event):

        if self.__is_zoom_out_finished:
            # 更新当前控件的几何信息
            self.__geometry_before_zoom = self.geometry()
            self.__font_size_before_zoom = self.font().pointSizeF()
        else:
            self.zoom_out_group.stop()

        # 形状放大。不关心动画的起始值是什么，只在乎动画的结束值必须是所有动画开始前的控件大小的zoom_factor倍
        start_rect = self.geometry()
        stop_rect = self.cal_zoom_in_rect()
        self.zoom_in_geometry.setStartValue(start_rect)
        self.zoom_in_geometry.setEndValue(stop_rect)

        # 字体放大。
        start_font_size = self.font().pointSizeF()
        stop_font_size = self.__font_size_before_zoom * self.__zoom_factor_font
        self.zoom_in_font.setStartValue(start_font_size)
        self.zoom_in_font.setEndValue(stop_font_size)

        print('started', self.geometry())
        print('计算后', stop_rect)
        self.zoom_in_group.start()
        self.__is_zoom_in_finished = False
        pass

    def leaveEvent(self, event):
        self.__is_zoom_in_finished = True
        if not self.__is_zoom_in_finished:
            self.zoom_in_group.stop()

        # 形状缩小。巧了，这个只关注动画的最初值
        start_rect = self.geometry()
        stop_rect = self.__geometry_before_zoom
        self.zoom_out_geometry.setStartValue(start_rect)
        self.zoom_out_geometry.setEndValue(stop_rect)

        # 字体放大。
        start_font_size = self.font().pointSizeF()
        stop_font_size = self.__font_size_before_zoom
        self.zoom_out_font.setStartValue(start_font_size)
        self.zoom_out_font.setEndValue(stop_font_size)

        self.zoom_out_group.start()
        self.__is_zoom_out_finished = False
        pass

    @pyqtProperty(float)
    def font_size(self):
        return self.font().pointSizeF()

    @font_size.setter
    def font_size(self, value):
        font = self.font()
        font.setPointSizeF(value)
        self.setFont(font)

    @pyqtProperty(QRect)
    def cus_geometry(self):
        return self.geometry()

    @cus_geometry.setter
    def cus_geometry(self, value):
        self.value = value
        self.setGeometry(value)


    # def zoom_in_finish(self):
    #     self.__is_zoom_in_finished = True
    #     self.zoom_in_finished.emit()


    def zoom_out_finish(self):
        self.__is_zoom_out_finished = True


    def cal_zoom_in_rect(self):
        center_point = self.__geometry_before_zoom.center()
        end_width = self.__geometry_before_zoom.width() * self.__zoom_factor_rect
        end_height = self.__geometry_before_zoom.height() * self.__zoom_factor_rect
        return QRect(
            center_point.x() - end_width // 2,  # 新左上角 x 坐标
            center_point.y() - end_height // 2,  # 新左上角 y 坐标
            end_width,  # 新宽度
            end_height  # 新高度
        )

    def sizeHint(self):
        if self.__is_zoom_in_finished:
            return super().sizeHint()
        return self.value.size()



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.ui_style()
        pass

    # 初始化时的控件显示
    def setup_ui(self):
        # MainWindow的中心控件
        self.wd_central_widget = QWidget()
        self.setCentralWidget(self.wd_central_widget)
        self.hl_layout = QHBoxLayout(self.wd_central_widget)

        self.pb_test_1 = HoverLargeButton("测试按钮1")
        self.pb_test_2 = HoverLargeButton("测试按钮2")
        self.pb_test_3 = HoverLargeButton("测试按钮3")

        self.hl_layout.addStretch(1)
        self.hl_layout.addWidget(self.pb_test_1)
        self.hl_layout.addStretch(1)
        self.hl_layout.addWidget(self.pb_test_2)
        self.hl_layout.addStretch(1)
        self.hl_layout.addWidget(self.pb_test_3)
        self.hl_layout.addStretch(1)

        pass

    # 控件样式
    def ui_style(self):
        pass

    def test_clicked(self):
        print('father', self.pb_test_1.geometry())
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.showMaximized()
    sys.exit(app.exec_())

