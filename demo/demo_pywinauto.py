
from pywinauto.application import Application

app = Application(backend="uia").connect(title_re="qt_nature")
# 或者
# app = Application(backend="uia").start(r"python \auto_demo_qt.py")

# 等待窗口出现
app_dialog = app.window(title_re="qt_nature")
app_dialog.wait('ready')

# 与窗口进行交互
print(app_dialog["btn_test"].rectangle())  # 假设有一个名为 Button1 的按钮
print(app_dialog["prompt_dialog"].rectangle())
# app_dialog.Edit1.set_text('Some text')  # 假设有一个名为 Edit1 的输入框


