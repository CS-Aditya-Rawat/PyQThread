import sys
import time
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QProgressBar, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot


class ThreadClass(QThread):
    # any_signal = pyqtSignal(int)
    started = pyqtSignal(str)
    progress_value = pyqtSignal(int)
    progress_text = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        self.started.emit(f"Starting thread.. {self.index}")
        for i in range(100):
            time.sleep(0.2)
            self.progress_value.emit(i + 1)
            self.progress_text.emit(f"Task {self.index} >>> {i+1}")

        self.progress_text.emit(f"Thread... {self.index} Completed Successfully.")
        self.finished.emit(f"Thread... {self.index} Completed Successfully.")

    def stop(self):
        self.started.emit(f"Trying to Stop Thread... {self.index}")
        self.finished.emit(f"Successfully Stopped Thread... {self.index}")
        self.progress_value.emit(0)
        self.is_running = False
        self.terminate()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("thread.ui", self)

        self.threads = {}
        self.progress_bars = [
            self.ui.progressBar,
            self.ui.progressBar_2,
            self.ui.progressBar_3,
            self.ui.progressBar_4,
            self.ui.progressBar_5,
            self.ui.progressBar_6,
        ]

        for progress_bar in self.progress_bars:
            progress_bar.setMaximum(100)
            progress_bar.setMinimum(0)
            progress_bar.setValue(0)

        self.start_buttons = [
            self.ui.start_t1_btn,
            self.ui.start_t2_btn,
            self.ui.start_t3_btn,
            self.ui.start_t4_btn,
            self.ui.start_t5_btn,
            self.ui.start_t6_btn,
        ]
        self.stop_buttons = [
            self.ui.stop_t1_btn,
            self.ui.stop_t2_btn,
            self.ui.stop_t3_btn,
            self.ui.stop_t4_btn,
            self.ui.stop_t5_btn,
            self.ui.stop_t6_btn,
        ]
        self.init_signal_slot()

    def init_signal_slot(self):
        for i, start_button in enumerate(self.start_buttons, start=1):
            start_button.clicked.connect(lambda _, idx=i: self.start_task(idx))

        for i, stop_button in enumerate(self.stop_buttons, start=1):
            stop_button.clicked.connect(lambda _, idx=i: self.stop_task(idx))

    def update_status(self, task_id, text):
        list_widget = self.ui.listWidget
        if task_id > 3:
            list_widget = self.ui.listWidget_2
        list_widget.addItem(text)
        list_widget.scrollToBottom()

    def toggle_button(self, task_id, enable=True):
        self.start_buttons[task_id - 1].setEnabled(enable)

    def update_progress(self, value, task_id):
        self.progress_bars[task_id - 1].setValue(value)

    def start_task(self, task_id):
        thread = ThreadClass(parent=None, index=task_id)

        thread.started.connect(lambda text: self.update_status(task_id, text))
        thread.started.connect(lambda: self.toggle_button(task_id, enable=False))
        thread.progress_value.connect(
            lambda value: self.update_progress(value, task_id)
        )
        thread.progress_text.connect(lambda text: self.update_status(task_id, text))
        thread.finished.connect(lambda: self.toggle_button(task_id, enable=True))

        self.threads[task_id] = thread
        thread.start()

    def stop_task(self, task_id):
        try:
            thread = self.threads[task_id]
            thread.progress_value.connect(
                lambda value: self.update_progress(value, task_id)
            )
            thread.finished.connect(lambda text: self.update_status(task_id, text))
            thread.finished.connect(lambda: self.toggle_button(task_id, enable=True))
            thread.stop()
        except KeyError:
            self.show_popup("Error", f"Thread {task_id} is not running.")

    def show_popup(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


app = QApplication(sys.argv)
w = Window()
w.show()
sys.exit(app.exec())
