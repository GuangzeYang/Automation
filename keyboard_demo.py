import keyboard


def on_key_event(e):
    print(f"Key {e.name} pressed")


if __name__ == '__main__':
    keyboard.on_press(on_key_event)  # 监听按键按下事件
    keyboard.wait("esc")
    pass