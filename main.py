import sys

from PyQt5.QtWidgets import QApplication
from driver.main_driver import AutoDrive

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoDrive()
    window.show()
    sys.exit(app.exec_())
