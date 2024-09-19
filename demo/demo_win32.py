import win32con
import win32gui
from typing import List

def enum_window_callback(hwnd, result):
    window_text = win32gui.GetWindowText(hwnd)
    if window_text:
        result.append((hwnd, window_text))


def get_handle_all() -> List[tuple]:
    '''
    获得当前所有窗口句柄
    :return: list
    '''
    result = []
    win32gui.EnumWindows(enum_window_callback, result)
    return result


def enum_child_handle(hwnd, result):
    child_handle = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
    print(child_handle)
    pass

def get_child_handle(parent_hwnd):
    hwndChildList = []
    win32gui.EnumChildWindows(parent_hwnd, enum_child_handle, hwndChildList)
    return hwndChildList


if __name__ == '__main__':
    wechat_handle = win32gui.FindWindow(None, 'qt_nature')
    print(wechat_handle)
    print(get_child_handle(wechat_handle))
    left, top, right, bottom = win32gui.GetWindowRect(wechat_handle)
    print(left, top, right, bottom)
    win32gui.ShowWindow(wechat_handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(wechat_handle)
    win32gui.SetActiveWindow(wechat_handle)

    # 取消置顶
    # win32gui.SetWindowPos(wechat_handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,win32con.SWP_SHOWWINDOW|win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)
    pass



# if __name__ == '__main__':
#     import win32gui
#
#
#     # 回调函数，用于处理每个子控件
#     def enum_child_windows_callback(hwnd, child_windows):
#         # 获取子控件的标题
#         window_text = win32gui.GetWindowText(hwnd)
#         # 获取子控件的类名
#         class_name = win32gui.GetClassName(hwnd)
#
#         # 将子控件的句柄及其信息添加到列表中
#         child_windows.append({
#             'hwnd': hwnd,
#             'title': window_text,
#             'class_name': class_name
#         })
#
#
#     # 获取父窗口的句柄（例如，通过窗口标题）
#     parent_window_title = "qt_nature"
#     parent_hwnd = win32gui.FindWindow(None, parent_window_title)
#     print(parent_hwnd)
#
#     if not parent_hwnd:
#         print("未找到父窗口")
#     else:
#         # 存储子控件句柄的列表
#         child_windows = []
#
#         # 枚举父控件中的所有子控件
#         win32gui.EnumChildWindows(parent_hwnd, enum_child_windows_callback, child_windows)
#         print('child_windows', child_windows)
#         # 打印所有子控件的信息
#         for child in child_windows:
#             print(f"子控件句柄: {child['hwnd']}, 标题: {child['title']}, 类名: {child['class_name']}")
#
#     ...
