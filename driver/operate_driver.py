
from gui.operate_gui import OperateGui


class OperateDriver(OperateGui):

    def __init__(self):
        super().__init__()
        self.bind_signal_slot()
        pass

    def bind_signal_slot(self):
        self.open_file_action.triggered.connect(self.open_file)
        self.save_file_action.triggered.connect(self.save_file)
        self.pb_start_execution.clicked.connect(self.start_execution)
        self.pb_stop_execution.clicked.connect(self.stop_execution)
        self.pb_continue_execution.clicked.connect(self.continue_execution)
        self.pb_pause_execution.clicked.connect(self.pause_execution)

    def open_file(self):
        pass

    def save_file(self):
        pass

    def start_execution(self):
        pass

    def stop_execution(self):
        pass

    def pause_execution(self):
        pass

    def continue_execution(self):
        pass
