import sys

from datetime import datetime
import enum
from typing import Union

import yaml
from loguru import logger
from PyQt5.QtWidgets import QApplication
from driver.main_driver import AutoDrive
from driver.custom_enum import OperateType, OperateAction

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

def enum_representer(tag_name:str):
    def representer(dumper, data):
        return dumper.represent_scalar(f'!{tag_name}', data.name)
    return representer

def enum_constructor(enum_type:Union[OperateType, OperateType]):
    def constructor(loader, node):
        value = node.value  # 提取节点的值
        return enum_type[value]  # 返回对应的枚举实例
    return constructor

operate_type_representer = enum_representer('OperateType')
operate_action_representer = enum_representer('OperateAction')
operate_type_constructor = enum_constructor(OperateType)
operate_action_constructor = enum_constructor(OperateAction)

yaml.add_representer(OperateType, operate_type_representer)
yaml.add_representer(OperateAction, operate_action_representer)
yaml.add_constructor('!OperateType', operate_type_constructor)
yaml.add_constructor('!OperateAction', operate_action_constructor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoDrive()
    window.show()
    sys.exit(app.exec_())
