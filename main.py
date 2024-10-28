import sys

from datetime import datetime
from loguru import logger
from PyQt5.QtWidgets import QApplication
from driver.main_driver import AutoDrive

logger_handle_info = logger.add(
    sink=f'./static/logs/{datetime.now().strftime("%Y-%m-%d")}.log',
    level='INFO',   # 当前的日志级别
    format='{time:HH:mm:ss}-{level}-{module}-{line}-{message}',
    retention='7 days',
    encoding='utf-8'
)
# debug 级别的日志
logger_handle_debug = logger.add(
    sink=f'./static/logs/{datetime.now().strftime("%Y-%m-%d")}_debug.log',
    level='DEBUG',   # 当前的日志级别
    format='{time:HH:mm:ss}-{level}-{message}',
    retention='7 days',
    encoding='utf-8'
)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoDrive()
    window.show()
    sys.exit(app.exec_())
