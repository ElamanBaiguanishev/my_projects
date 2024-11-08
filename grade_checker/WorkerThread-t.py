import time
import traceback

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import json
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog, QGridLayout, QPushButton
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from network import change_ip
from tools import log_exception


class WorkerThread_test(QThread):
    signal_error = pyqtSignal(str)
    choice_error = pyqtSignal(str)
    update_progress_signal = pyqtSignal(int, str)

    def __init__(self, service):
        super().__init__()
        self.current_group = None
        self.semester = None
        with open("resources/network.json") as json_file:
            data_json = json.load(json_file)
            self.ip = data_json["reload_ip"]
        self.checked_widgets = []
        self.path = ""
        self.button_name = ""
        self.is_running = None
        self.is_cycle = False

        self.options = Options()

        self.options.add_argument(
            "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        self.service = service
        self.driver = None

    def set_arguments(self, checked_widgets, path, button_name, semester, current_group):
        self.checked_widgets = checked_widgets
        self.path = path
        self.button_name = button_name
        self.semester = semester
        self.current_group = current_group

    def run(self):
        try:
            if self.button_name == "Зачетка":
                self.record_book_selenium()
            elif self.button_name == "Долги":
                self.debts_selenium()
            else:
                self.signal_error.emit("Invalid button name")
        except Exception as e:
            self.signal_error.emit(str(e))

    def record_book_selenium(self):
        for i, json_object in enumerate(self.checked_widgets, start=1):
            if not self.is_running:
                print("Конец цикла")
                break
            json_valid = json.loads(json_object)
            fio = json_valid[0]
            self.update_progress_signal.emit(i, fio)
            valid = json_valid[1]
            print(valid, "началось")
            self.options.headless = True
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            semestr = self.semester
            group = self.current_group
            screenshots_path = f"{self.path}/{semestr}/{group}/Зачетная книжка/"
            screenshots_path = screenshots_path.replace("\\", "/")

            if not os.path.exists(screenshots_path):
                os.makedirs(screenshots_path)

            self.driver.get("https://xn--d1ahgpw.xn--p1ai/kabinet.php")

            try:
                main_input = self.driver.find_element(By.CSS_SELECTOR,
                                                      "input[type='text'][class='input-at'][name='shifr']")
                main_input.send_keys(valid)
                ok_button = self.driver.find_element(value="login")
                time.sleep(10)

                ok_button.click()

                time.sleep(10)

                sem = self.driver.find_element(By.CSS_SELECTOR, f"a[href='#home{self.semester}']")
                sem.click()

                info_div = self.driver.find_element(by=By.CSS_SELECTOR, value="div[class='tab-content']")

                div_element = self.driver.find_element(value=f"home{self.semester}")

                self.driver.execute_script('document.body.innerHTML = arguments[0]',
                                           info_div.get_attribute('outerHTML') + div_element.get_attribute('outerHTML'))

                sc = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
                self.driver.set_window_size(sc('Width'),
                                            sc('Height'))
                self.driver.find_element(by=By.TAG_NAME, value='body').screenshot(f"{screenshots_path}/{fio}.png")

                if self.ip:
                    change_ip()

                self.driver.quit()
                print(valid, "конец")
            except Exception as e:
                if self.driver is None:
                    break
                sc = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
                self.driver.set_window_size(sc('Width'), sc('Height'))
                self.driver.find_element(by=By.TAG_NAME, value='body').screenshot(
                    f"{screenshots_path}/{fio}.ошибка.png")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                log_exception(exc_type, exc_value, exc_traceback)
                self.choice_error.emit(f"Ошибка на шаге {json_object}")
                traceback.print_exc()
                self.is_cycle = True
                self.wait_for_response()
                if not self.is_running:
                    break
                continue

    def debts_selenium(self):
        for i, json_object in enumerate(self.checked_widgets, start=1):
            if not self.is_running:
                print("Конец цикла")
                break
            json_valid = json.loads(json_object)
            fio = json_valid[0]
            self.update_progress_signal.emit(i, fio)
            valid = json_valid[1]
            print(valid, "началось")
            self.options.headless = True
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            semestr = self.semester
            group = self.current_group
            screenshots_path = f"{self.path}/{semestr}/{group}/Долги/"
            screenshots_path = screenshots_path.replace("\\", "/")

            if not os.path.exists(screenshots_path):
                os.makedirs(screenshots_path)

            self.driver.get("https://xn--d1ahgpw.xn--p1ai/kabinet.php")

            try:
                main_input = self.driver.find_element(By.CSS_SELECTOR,
                                                      "input[type='text'][class='input-at'][name='shifr']")
                main_input.send_keys(valid)
                ok_button = self.driver.find_element(value="login")

                time.sleep(10)

                ok_button.click()

                time.sleep(10)

                menu = self.driver.find_element(By.CSS_SELECTOR, "ul[class='nav nav-pills nav-fill d-md-flex']")

                semesters = menu.find_elements(by=By.XPATH, value="./*")

                info_div = self.driver.find_element(by=By.CSS_SELECTOR, value="div[class='tab-content']")

                dolgi_div = ""
                for semester in semesters:
                    semester.click()
                    div = self.driver.find_element(value=f"home{semester.text}")
                    red = div.find_elements(By.CSS_SELECTOR, "div[style*='background: #ffd5d5;']")
                    if red:
                        for r in red:
                            dolgi_div += r.get_attribute('outerHTML')

                self.driver.execute_script('document.body.innerHTML = arguments[0]',
                                           info_div.get_attribute('outerHTML') + dolgi_div)
                sc = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
                self.driver.set_window_size(sc('Width'),
                                            sc('Height'))
                self.driver.find_element(by=By.TAG_NAME, value='body').screenshot(f"{screenshots_path}/{fio}.png")

                self.driver.quit()

                if self.ip:
                    change_ip()

                print(valid, "конец")
            except Exception as e:
                if self.driver is None:
                    break
                sc = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
                self.driver.set_window_size(sc('Width'), sc('Height'))
                self.driver.find_element(by=By.TAG_NAME, value='body').screenshot(
                    f"{screenshots_path}/{fio}.ошибка.png")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                log_exception(exc_type, exc_value, exc_traceback)
                self.choice_error.emit(f"Ошибка на шаге {json_object}")
                traceback.print_exc()
                self.is_cycle = True
                self.wait_for_response()
                if not self.is_running:
                    break
                continue

    def wait_for_response(self):
        print("Начал ждать")
        while self.is_cycle:
            print("Жду")
            time.sleep(0.1)
