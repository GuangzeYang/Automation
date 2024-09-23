from PyQt5.QtCore import pyqtSignal

from gui.wizard_gui import WizardGui
from pynput.mouse import Listener as MListener
from pynput.keyboard import Listener as KListener, Key
import keyboard
import mouse

import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


class WizardDriver(WizardGui):
    open_operate = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        pass

    def show(self):
        super().show()
        self.mouse_listener = MListener(on_click=self.mouse_on_click, on_scroll=self.mouse_on_scroll)
        self.keyboard_listener = KListener(on_press=self.keyboard_on_press, on_release=self.keyboard_on_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        pass

    def mouse_on_click(self, abs_x, abs_y, button, pressed):
        print("mouse_on_click", abs_x, abs_y, button, pressed)
        pass

    def mouse_on_scroll(self, abs_x, abs_y, dx, dy):
        print('mouse_on_scroll', abs_x, abs_y, dx, dy)
        pass


    def keyboard_on_press(self, key):
        print("keyboard_on_press", key)
        pass

    def keyboard_on_release(self, key):
        print('keyboard_on_release', key, str(key))
        if key == Key.esc:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            self.open_operate.emit()
        pass

