import win32con
import win32gui
import pyautogui


if __name__ == '__main__':
    # 通过pywin32拿到父窗口句柄，并将其显示在最前，获取坐标
    wechat_handle = win32gui.FindWindow(None, 'qt_nature')
    win32gui.ShowWindow(wechat_handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(wechat_handle)
    left, top, right, bottom = win32gui.GetWindowRect(wechat_handle)
    print(left, top, right, bottom)

    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.3
    pyautogui.moveTo(left+100, bottom-400, duration=0.2)
    # pyautogui.click()
    pass