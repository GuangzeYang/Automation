
from driver.wizard_driver import WizardDriver
from driver.operate_driver import OperateDriver

class AutoDrive:

    def __init__(self):
        super().__init__()
        self.operate_driver = OperateDriver()
        self.wizard_driver = WizardDriver()
        pass

    def show(self):
        self.operate_driver.show()
        pass