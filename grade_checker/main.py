import sys
from PyQt5.QtWidgets import QApplication

from Config import Config
from tools import create_log_file, log_exception

app = QApplication(sys.argv)

if __name__ == '__main__':
    try:
        log_filename = create_log_file()
        sys.excepthook = log_exception
        mainWindow = Config()
        mainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log_exception(exc_type, exc_value, exc_traceback)
