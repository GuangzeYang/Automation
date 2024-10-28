import time

from pynput.keyboard import Listener as KListener
from pynput.keyboard import Controller as KController
from pynput.mouse import Listener as MListener, Button

import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


def on_click(x, y, button, pressed):
    if button == Button.left:
        print(x, y)
    print(button, type(button))                              
                                                             
if __name__ == '__main__':
    mouse_listener = MListener(on_click=on_click)
    mouse_listener.start()
    mouse_listener.join()
    pass
