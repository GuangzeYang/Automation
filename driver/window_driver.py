import win32con
import win32gui
from typing import List


class WindowDriver:

    def __init__(self, window_title):
        super().__init__()
        # 窗口句柄
        self.init_hwnd(window_title)
        pass

    def init_hwnd(self, window_title):
        self.hwnd = win32gui.FindWindow(None, window_title)
        print('窗口句柄为：', self.hwnd)
        ...

    def get_window_rect(self):
        '''将隐藏的窗口提到屏幕前面来，而后返回rect信息'''
        # 将窗口显示
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        # 将窗口提前
        win32gui.SetForegroundWindow(self.hwnd)
        return win32gui.GetWindowRect(self.hwnd)

    def get_handle_all(self) -> List[tuple]:
        '''
        获得当前所有窗口句柄
        :return: list
        '''
        result = []
        win32gui.EnumWindows(self.enum_handle_callback, result)
        return result

    def enum_handle_callback(self, result):
        window_text = win32gui.GetWindowText(self.hwnd)
        if window_text:
            result.append((self.hwnd, window_text))
        ...

    def get_child_handle(self):
        hwndChildList = []
        win32gui.EnumChildWindows(self.hwnd, self.enum_child_handle, hwndChildList)
        return hwndChildList

    def enum_child_handle(self, result):
        child_handle = win32gui.GetWindow(self.hwnd, win32con.GW_CHILD)
        result.append(child_handle)
        ...


if __name__ == "__main__":
    # 获取父窗口的句柄（例如，通过窗口标题）
    parent_window_title = "钉钉"
    window_driver = WindowDriver(parent_window_title)
    window_rect = window_driver.get_window_rect()
    print(window_rect)
    ...
