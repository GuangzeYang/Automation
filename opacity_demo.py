import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget


# 自定义的异常处理函数
def my_exception_handler(exc_type, exc_value, exc_tb):
    # 捕获所有未处理的异常
    if exc_type is not KeyboardInterrupt:
        # 创建一个消息框显示异常信息
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        QMessageBox.critical(None, "异常", f"程序发生了未处理的异常:\n\n{error_msg}")


# 设置全局异常处理器
sys.excepthook = my_exception_handler


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('全局异常捕获示例')
        self.setGeometry(100, 100, 400, 300)

    def mousePressEvent(self, event):
        # 故意引发一个异常
        raise ValueError("故意触发异常！")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 你可以在应用的任何地方引发异常，这里是一个示例
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
