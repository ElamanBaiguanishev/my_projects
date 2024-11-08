from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QProgressBar, QApplication


class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        icon = QIcon('resources/favicon.ico')
        self.setWindowIcon(icon)
        self.progress_bar = self.create_progress_bar()
        self.status_label = QLabel("Обновление базы семестров...")

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        self.setWindowTitle("Прогресс операции")

    def create_progress_bar(self):
        progress_bar = QProgressBar(self)
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setMinimumWidth(300)
        return progress_bar

    def update_progress(self, progress_value):
        int_progress_value = int(progress_value)
        self.progress_bar.setValue(int_progress_value)
        QApplication.processEvents()
