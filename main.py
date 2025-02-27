import sys

from datetime import datetime
from typing import Union

import yaml
from PyQt5.QtCore import QSharedMemory, Qt
from loguru import logger
from PyQt5.QtWidgets import QApplication, QMessageBox
from yaml import Dumper, MappingNode, Loader, ScalarNode
from qfluentwidgets import Dialog
from screeninfo import get_monitors


from driver.main_driver import AutoDrive
from driver.auto_dataclass import OperateAction, MouseAction, KeyboardAction

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
def operate_type_representer(dumper:Dumper, data:OperateAction):
    return dumper.represent_scalar('!OperateAction', data.name)

def operate_type_constructor(loader:Loader, node:ScalarNode):
    value = loader.construct_scalar(node)
    return OperateAction[value]

def keyboard_representer(dumper:Dumper, action:KeyboardAction):
    mapping_node = {'key': action.key, 'action': action.action, 'delay': action.delay,
                    'is_checked': action.is_checked, "list_item_id":action.list_item_id}
    return dumper.represent_mapping('!KeyboardAction', mapping_node)

def keyboard_constructor(loader:Loader, node:MappingNode):
    value = loader.construct_mapping(node)  # 提取节点的值
    return KeyboardAction(value["key"], value["action"], value["delay"], value["is_checked"], value["list_item_id"])  # 返回对应的枚举实例

def mouse_representer(dumper:Dumper, action:MouseAction):
    mapping_node = {'button': action.button, 'action': action.action, "x_pos":action.x_pos, "y_pos":action.y_pos,
                    'delay': action.delay, 'is_checked': action.is_checked, 'scroll_dx':action.scroll_dx,
                    'scroll_dy':action.scroll_dy, "list_item_id":action.list_item_id}
    return dumper.represent_mapping('!MouseAction', mapping_node)

def mouse_constructor(loader:Loader, node:MappingNode):
    value = loader.construct_mapping(node)  # 提取节点的值
    return MouseAction(value["action"], value["x_pos"], value["y_pos"], value["delay"], value["is_checked"],
                       value["button"], value["scroll_dx"], value["scroll_dy"], value["list_item_id"])  # 返回对应的枚举实例

yaml.add_representer(KeyboardAction, keyboard_representer)
yaml.add_representer(MouseAction, mouse_representer)
yaml.add_representer(OperateAction, operate_type_representer)
yaml.add_constructor('!KeyboardAction', keyboard_constructor)
yaml.add_constructor('!MouseAction', mouse_constructor)
yaml.add_constructor('!OperateAction', operate_type_constructor)

def global_exception_handler(exc_type, exc_value, exc_tb):
    QMessageBox.critical(None, "错误", f"完蛋啦！！当前操作出现错误：\n{exc_value}").exec()

class SingleApplication(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.shared_memory = QSharedMemory("unique_app_id")

        if self.shared_memory.attach():
            print("Another instance is already running!")
            QMessageBox.critical(None, "错误", "程序已启动！")
            sys.exit(0)
        else:
            self.shared_memory.create(1)

    def release_lock(self):
        self.shared_memory.detach()

if __name__ == '__main__':
    screen_width = get_monitors()[0].width
    screen_height = get_monitors()[0].height
    if screen_width > 3000:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = SingleApplication(sys.argv)
    window = AutoDrive(app.release_lock)
    # 设置全局异常处理器
    sys.excepthook = global_exception_handler
    window.show()
    sys.exit(app.exec_())
