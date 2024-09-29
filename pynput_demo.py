import time

from pynput.keyboard import Listener as KListener
from pynput.keyboard import Controller as KController

import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

def on_press(key):
    print(key)

if __name__ == '__main__':
    key_controller = KController()
    key_listener = KListener(on_press=on_press)
    key_listener.start()
    key_listener.join(2)
    key_listener.stop()
    key_listener.stop()
    print(1111111111)

    pass
