"""工作线程模块，用于执行耗时操作"""
from PySide6.QtCore import QThread, Signal


class WorkerThread(QThread):
    """工作线程，用于执行耗时操作"""
    log_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, update_func, msh_path, case_path, env_source=None):
        super().__init__()
        self.update_func = update_func
        self.msh_path = msh_path
        self.case_path = case_path
        self.env_source = env_source

    def run(self):
        try:
            success = self.update_func(self.msh_path, self.case_path, logger=self.log_signal.emit, env_source=self.env_source)
            self.finished_signal.emit(success, "")
        except Exception as e:
            self.finished_signal.emit(False, str(e))