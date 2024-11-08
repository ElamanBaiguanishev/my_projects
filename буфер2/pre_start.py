import functools
import json
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QHBoxLayout, QMessageBox, \
    QCheckBox

from Indicator import Indicator
from checked import check_db, check_access
from main import MainWindow, ProgressDialog
from parsing import data
from tools import *
from PyQt5.QtWidgets import QLabel, QLineEdit
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


class PathWidget(QWidget):
    def __init__(self, name, func_check, path_name):
        super().__init__()
        self.path_name = path_name
        self.name = name
        self.func_check = func_check
        self.indicator = Indicator()
        self.path_db = QLineEdit(self)
        self.label_errors = QLabel()
        self.main_layout = QGridLayout()
        self.up_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.up_layout, 0, 0)
        self.main_layout.addWidget(self.label_errors, 1, 0)
        self.init_ui()

    def init_ui(self):
        label = QLabel(self.name)
        self.path_db.setReadOnly(True)

        browse_button = QPushButton('Обзор', self)
        browse_button.clicked[bool].connect(self.choose_folder)

        self.up_layout.addWidget(label)
        self.up_layout.addWidget(self.path_db)
        self.up_layout.addWidget(browse_button)
        self.up_layout.addWidget(self.indicator)

        with open("resources/path.json") as json_file:
            # Загружаем данные из JSON-файла
            data_ = json.load(json_file)
            path = data_[self.path_name]

        if path is not None:
            res = self.func_check(path)
            if not res["Access"]:
                self.label_errors.setText("Нет доступа к папке")
                self.indicator.toggle_value(False)
            elif len(res["Errors"]) != 0:
                self.label_errors.setText("\n".join(res["Errors"]))
                self.indicator.toggle_value(False)
            else:
                self.label_errors.setText("")
                self.path_db.setText(path)
                self.indicator.toggle_value(True)

    def choose_folder(self):
        folder_dialog = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_dialog:
            self.path_db.setText(folder_dialog)
        else:
            folder_dialog = self.path_db.text()
        res = self.func_check(folder_dialog)
        if not res["Access"]:
            self.label_errors.setText("Нет доступа к папке")
            self.indicator.toggle_value(False)
        elif len(res["Errors"]) != 0:
            self.label_errors.setText("\n".join(res["Errors"]))
            self.indicator.toggle_value(False)
        else:
            self.label_errors.setText("")
            with open("resources/path.json", "r+") as json_file:
                data = json.load(json_file)
                data[self.path_name] = folder_dialog
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()
            self.indicator.toggle_value(True)


class PreStart(QWidget):
    def __init__(self):
        super().__init__()
        self.time = None
        self.main_window = None
        self.path_db = PathWidget("База данных", check_db, "db")
        self.path_db1 = PathWidget("База ответы", check_access, "answers")
        self.path_db2 = PathWidget("Скриншоты", check_access, "screenshots")
        self.service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.main_layout = QGridLayout()
        self.check_ip = QCheckBox("Менять айпи")
        self.check_time = QCheckBox("Время теста")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(600, 200, 568, 300)
        self.setStyleSheet("background: #f7f7f7")
        icon = QIcon('resources/favicon.ico')
        self.setWindowIcon(icon)
        self.setStyleSheet(open("resources/styles.qss").read())
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.path_db, 0, 0)
        self.main_layout.addWidget(self.path_db1, 1, 0)
        self.main_layout.addWidget(self.path_db2, 2, 0)

        self.check_ip.setChecked(False)
        self.main_layout.addWidget(self.check_ip, 3, 0)

        time_layout = QHBoxLayout()
        self.check_time.setChecked(False)
        time_layout.addWidget(self.check_time)

        time_changed = QLineEdit(self)
        time_changed.setPlaceholderText("Время прохожения теста в минутах")
        time_changed.textChanged.connect(functools.partial(self.set_time, time_change=time_changed))
        time_layout.addWidget(time_changed)

        self.main_layout.addLayout(time_layout, 4, 0)

        button_new_base = QPushButton("Обновить")
        button_new_base.clicked[bool].connect(self.new_base)
        self.main_layout.addWidget(button_new_base, 5, 0)

        button_start = QPushButton("Старт")
        button_start.clicked[bool].connect(self.start)
        self.main_layout.addWidget(button_start, 6, 0)

    def set_time(self, time_change):
        self.time = time_change.text().lower()

    def new_base(self):
        reply = QMessageBox.question(self, 'Config DataBase',
                                     'При подтверждении "Yes" будут загружены новые данные из Excel файлов',
                                     QMessageBox.Yes | QMessageBox.No)
        progress_dialog = None
        if reply == QMessageBox.Yes:
            try:
                progress_dialog = ProgressDialog()
                progress_dialog.show()
                data(True, progress_dialog.update_progress)
            except FileNotFoundError as e_:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"Файл по пути: {e_.filename} не найден")
                log_exception(exc_type, exc_value, exc_traceback)
                progress_dialog.close()
            except:
                # Получение информации об исключении
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                             f"Тип исключения:, {exc_type}\n"
                             f"Сообщение об ошибке:, {exc_value}")
                log_exception(exc_type, exc_value, exc_traceback)
                progress_dialog.close()

    def start(self):
        if self.path_db.indicator.value and self.path_db1.indicator.value and self.path_db2.indicator.value:
            self.hide()
            self.main_window = MainWindow(self.check_ip.isChecked(), self, self.service, self.check_time.isChecked(),
                                          self.time)
        else:
            self.warning("Убедитесь, что есть доступ к папкам")

    def warning(self, text: str):
        QMessageBox.warning(self, "Warning", text)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        log_filename = create_log_file()
        sys.excepthook = log_exception
        mainWindow = PreStart()
        mainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log_exception(exc_type, exc_value, exc_traceback)
