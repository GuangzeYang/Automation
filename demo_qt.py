from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个菜单栏
        menu_bar = self.menuBar()

        # 设置菜单栏的样式表
        menu_bar.setStyleSheet("""
            QMenuBar {
                border-bottom: 1px solid; /* 设置底部分割线的宽度为2像素，颜色为黑色 */
            }
        """)

        # 添加一些菜单项以便于观察效果
        file_menu = menu_bar.addMenu('File')
        edit_menu = menu_bar.addMenu('Edit')

if __name__ == '__main__':
    app = QApplication([])

    main_win = MainWindow()
    main_win.show()

    app.exec_()