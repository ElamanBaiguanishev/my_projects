import json
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QCheckBox, QMessageBox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from PathWidget import PathWidget
from ProgressDialog import ProgressDialog
from parsing import data
from tools import check_db, check_access, log_exception
from MainWindow import MainWindow


class Config(QWidget):
    def __init__(self):
        super().__init__()
        self.check_ip = QCheckBox("Менять айпи")
        self.main_window = None
        self.main_layout = QGridLayout()

        chromedriver_path = "resources/chromedriver.exe"

        self.service = webdriver.chrome.service.Service(chromedriver_path)

        self.path_db = PathWidget("База данных", check_db, "db")
        self.path_db2 = PathWidget("Скриншоты", check_access, "screenshots")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Config')
        self.setGeometry(600, 200, 568, 300)
        self.setStyleSheet("background: #f7f7f7")
        icon = QIcon('resources/favicon.ico')
        self.setWindowIcon(icon)
        self.setStyleSheet(open("resources/styles.qss").read())
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.path_db, 0, 0)
        self.main_layout.addWidget(self.path_db2, 2, 0)
        with open("resources/network.json") as json_file:
            data_json = json.load(json_file)
            ip = data_json["reload_ip"]
        self.check_ip.setChecked(ip)
        self.main_layout.addWidget(self.check_ip, 3, 0)

        button_start = QPushButton("Старт")
        button_start.clicked[bool].connect(self.start)
        self.main_layout.addWidget(button_start, 5, 0)

        button_new_base = QPushButton("Обновить")
        button_new_base.clicked[bool].connect(self.new_base)
        self.main_layout.addWidget(button_new_base, 4, 0)

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
        with open("resources/network.json", "r+") as json_file:
            change = json.load(json_file)
            change["reload_ip"] = self.check_ip.isChecked()
            json_file.seek(0)
            json.dump(change, json_file, indent=4)
            json_file.truncate()
        if self.path_db.indicator.value and self.path_db2.indicator.value:
            self.hide()
            self.main_window = MainWindow(self, self.service)
        else:
            self.warning("Убедитесь, что есть доступ к папкам")

    def warning(self, text: str):
        QMessageBox.warning(self, "Warning", text)
