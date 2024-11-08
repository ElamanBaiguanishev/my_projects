import sys
from json import JSONDecodeError

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QTabWidget, QMessageBox

from ProgressDialog import ProgressDialog
from Tab import Tab
from parsing import check_config, data
from tools import log_exception


class MainWindow(QWidget):
    def __init__(self, settings, service):
        super().__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.settings = settings
        self.service = service
        self.data = None
        self.main_layout = QGridLayout()
        self.tab_widget = QTabWidget()
        progress_dialog = None
        if not check_config():
            try:
                progress_dialog = ProgressDialog()
                progress_dialog.show()
                self.data = data(True, progress_dialog.update_progress)
                self.init_ui()
            except FileNotFoundError as e_:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"Файл по пути: {e_.filename} не найден")
                log_exception(exc_type, exc_value, exc_traceback)
                progress_dialog.close()
                self.close()
                self.settings.show()
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                             f"Тип исключения:, {exc_type}\n"
                             f"Сообщение об ошибке:, {exc_value}")
                log_exception(exc_type, exc_value, exc_traceback)
                progress_dialog.close()
                self.close()
                self.settings.show()
        else:
            try:
                self.data = data(False)
                self.init_ui()
            except JSONDecodeError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"Файл конфига для загрузки данных поврежден \n{e}")
                log_exception(exc_type, exc_value, exc_traceback)
            except FileNotFoundError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"Файл конфига не найден \n{e}")
                log_exception(exc_type, exc_value, exc_traceback)
                sys.exit()
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                             f"Тип исключения:, {exc_type}\n"
                             f"Сообщение об ошибке:, {exc_value}")
                log_exception(exc_type, exc_value, exc_traceback)
                sys.exit()

    def init_ui(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(600, 200, 568, 700)
        self.setStyleSheet("background: #f7f7f7")
        icon = QIcon('resources/favicon.ico')
        self.setWindowIcon(icon)

        self.setStyleSheet(open("resources/styles.qss").read())
        self.setLayout(self.main_layout)
        self.create_tabs()
        self.main_layout.addWidget(self.tab_widget, 1, 0)
        self.show()

    def create_tabs(self):
        for semester in self.data:
            self.tab_widget.addTab(Tab(semester, self.data, self.service), semester)

    def closeEvent(self, a0):
        self.settings.show()

    def warning(self, text: str):
        QMessageBox.warning(self, "Warning", text)
