from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QProgressBar, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt, QEventLoop, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Создаем прогресс-бар
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Создаем метку для отображения текущего значения прогресса
        self.progress_label = QLabel("Progress: 0%", self)
        layout.addWidget(self.progress_label)

        # Создаем кнопку для запуска прогресса
        start_button = QPushButton("Start Progress", self)
        start_button.clicked.connect(self.start_progress)
        layout.addWidget(start_button)

        self.progress_steps = 5  # Установите количество частей, которые вы хотите отобразить

    def start_progress(self):
        for step in range(1, self.progress_steps + 1):
            progress_value = int((step / self.progress_steps) * 100)
            self.progress_bar.setValue(progress_value)
            self.progress_label.setText(f"Progress: {progress_value}%")
            QApplication.processEvents()
            self.sleep(1000)  # Имитация работы

    def sleep(self, milliseconds):
        loop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec_()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
