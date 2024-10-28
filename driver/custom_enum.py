
import enum


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

