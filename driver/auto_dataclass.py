from dataclasses import dataclass, field
from pynput import keyboard, mouse
import enum
import typing


class OperateType(enum.Enum):
    MOUSE=1
    KEYBOARD=2
    TIME=3


class OperateAction(enum.Enum):
    CLICK = 1
    SCROLL = 2
    TAP = 3
    MOVE = 4
    DELAY = 5


@dataclass
class KeyboardAction:
    key: keyboard.Key
    action:OperateAction
    delay:float
    is_checked:bool = False
    list_item_id:int = -1
    pass

@dataclass
class MouseAction:
    action:OperateAction
    x_pos:float  # 鼠标x的绝对坐标
    y_pos:float  # 鼠标y的绝对坐标
    delay:float
    is_checked:bool = False
    button: typing.Union[mouse.Button, str] = ''
    scroll_dx:int = 0
    scroll_dy:int = 0
    list_item_id:int = -1
    pass