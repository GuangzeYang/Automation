
from pynput.keyboard import Listener as KListener

import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

if __name__ == '__main__':
    key_board_lis = KListener(on_press=lambda x: print(x))
    key_board_lis.start()
    key_board_lis.join()
    pass
