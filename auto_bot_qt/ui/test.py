import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, exc_traceback))


def create_log_file():
    log_filename = "error_log.txt"
    logging.basicConfig(filename=log_filename,
                        level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return log_filename


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Error Logging Example")
        self.setGeometry(100, 100, 300, 200)

        button = QPushButton("Generate Error", self)
        button.setGeometry(100, 80, 100, 30)
        button.clicked.connect(self.generate_error)

    def generate_error(self):
        # Генерируем исключение (ZeroDivisionError) для демонстрации
        result = 1 / 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_filename = create_log_file()
    sys.excepthook = log_exception  # Переопределение обработчика исключений
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
