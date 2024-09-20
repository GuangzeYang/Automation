
from driver.wizard_driver import WizardDriver
from driver.operate_driver import OperateDriver

class AutoDrive:

    def __init__(self):
        super().__init__()
        self.operate_driver = OperateDriver()
        self.wizard_driver = WizardDriver()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.operate_driver.open_wizard.connect(self.open_wizard)
        self.wizard_driver.open_operate.connect(self.open_operate)

    def show(self):
        self.operate_driver.show()
        pass

    def open_wizard(self):
        self.operate_driver.hide()
        self.wizard_driver.show()
        self.wizard_driver.setFocus()
        pass

    def open_operate(self):
        self.operate_driver.show()
        self.wizard_driver.hide()
        self.operate_driver.setFocus()
        pass