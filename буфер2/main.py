import functools
import json
import random
import sys
import textwrap
import threading
import traceback
from datetime import datetime
from json import JSONDecodeError
from selenium.webdriver.support import expected_conditions as EC

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QTabWidget, QLabel, QGroupBox, \
    QVBoxLayout, QDialog, QCheckBox, QMessageBox, QProgressBar, QScrollArea, QLineEdit, QInputDialog

from WorkerThread import WorkerThread
from approximate_answer import approximate, find_most_similar_answer
from network import change_ip
from parsing import data, check_config
from parse_answers import answers
import time

from selenium.webdriver.common.by import By
from selenium import webdriver

from status_bar import StatusBar
from tools import *
from selenium.webdriver.support.ui import WebDriverWait


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
        progress_bar.setMinimumWidth(300)  # Установим минимальную ширину прогресс бара
        return progress_bar

    def update_progress(self, progress_value):
        int_progress_value = int(progress_value)
        self.progress_bar.setValue(int_progress_value)
        QApplication.processEvents()  # Обновим содержимое диалогового окна


class MainWindow(QWidget):
    def __init__(self, ip, settings, service, is_time, choice_time):
        super().__init__()
        self.choice_time = choice_time
        self.is_time = is_time
        self.settings = settings
        self.ip = ip
        self.current_test_name = None
        self.current_group = None
        self.current_lesson = None
        self.students = None
        self.dict_semestr_lesson = None
        self.grid = None
        self.tests = None
        self.test_url = None
        self.users_name_checkbox_layout = None
        self.student_ids = None
        self.lessons = None
        self.current_semestr = None
        self.stop_flag = False
        self.thread = None
        self.tab_widget = QTabWidget()
        self.main_layout = QGridLayout()
        self.status_bar = StatusBar()
        self.main_layout.addWidget(self.status_bar, 2, 0)
        self.main_layout.addWidget(self.tab_widget, 1, 0)

        self.chrome_options = webdriver.ChromeOptions()

        self.service = service

        self.driver = None

        progress_dialog = None

        if not check_config():
            try:
                progress_dialog = ProgressDialog()
                progress_dialog.show()
                self.dict_semestr_lesson, self.students = data(True, progress_dialog.update_progress)
                self.init_ui()
            except FileNotFoundError as e_:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"Файл по пути: {e_.filename} не найден")
                log_exception(exc_type, exc_value, exc_traceback)
                progress_dialog.close()
                self.close()
                self.settings.show()
            except:
                # Получение информации об исключении
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
                self.dict_semestr_lesson, self.students = data(False)
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
                # Получение информации об исключении
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                             f"Тип исключения:, {exc_type}\n"
                             f"Сообщение об ошибке:, {exc_value}")
                log_exception(exc_type, exc_value, exc_traceback)
                sys.exit()

    def init_ui(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(600, 200, 568, 500)
        self.setStyleSheet("background: #f7f7f7")
        icon = QIcon('resources/favicon.ico')
        self.setWindowIcon(icon)

        self.setStyleSheet(open("resources/styles.qss", "r").read())

        self.setLayout(self.main_layout)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.create_tabs()
        self.show()

    def warning(self, text: str):
        QMessageBox.warning(self, "Warning", text)

    def tab_changed(self, index):
        try:
            self.status_bar.clear()
            text: QTabWidget = self.sender()
            widget = text.widget(index)
            layout = widget.layout()
            group_layout = layout.itemAt(1).widget().layout()
            test_layout = layout.itemAt(2).widget().layout()
            for i in reversed(range(group_layout.count())):
                group_layout.itemAt(i).widget().deleteLater()
            for i in reversed(range(test_layout.count())):
                test_layout.itemAt(i).widget().deleteLater()
        except:
            # Получение информации об исключении
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def create_tabs(self):
        try:
            for semestr in self.dict_semestr_lesson:
                tab = QWidget()
                grid = QGridLayout()
                tab_group = QGroupBox("Группы")
                tab_lessons = QGroupBox("Предметы")
                tab_tests = QGroupBox("Тесты")
                grid.addWidget(tab_group, 0, 0)
                grid.addWidget(tab_lessons, 0, 1)
                grid.addWidget(tab_tests, 0, 2)
                tab_layout_groups = QGridLayout()
                tab_layout_lessons = QVBoxLayout()
                tab_layout_tests = QVBoxLayout()
                tab_lessons.setLayout(tab_layout_lessons)
                tab_tests.setLayout(tab_layout_tests)

                groups = self.dict_semestr_lesson[semestr]
                row = 0
                col = 0
                for group in groups:
                    button = QPushButton(group)
                    button.setFixedSize(55, 25)
                    button.clicked.connect(
                        functools.partial(self.on_click_add_lesson, layout1=tab_layout_lessons,
                                          layout2=tab_layout_tests))
                    button.setObjectName(semestr)
                    tab_layout_groups.addWidget(button, row, col)
                    col += 1
                    if col == 2:
                        row += 1
                        col = 0
                tab_group.setLayout(tab_layout_groups)
                tab.setLayout(grid)
                self.tab_widget.addTab(tab, semestr)
        except:
            # Получение информации об исключении
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def on_click_add_lesson(self, layout1, layout2):
        try:
            for i in reversed(range(layout1.count())):
                layout1.itemAt(i).widget().deleteLater()
            for i in reversed(range(layout2.count())):
                layout2.itemAt(i).widget().deleteLater()
            button_sender = self.sender()
            semestr = button_sender.objectName()
            self.current_semestr = semestr
            group = button_sender.text()
            self.status_bar.set_group(group)
            self.lessons = self.dict_semestr_lesson[semestr][group]["lessons"]
            for i in self.lessons:
                # wrapped_text = "\n".join(textwrap.wrap(i, width=20))  # разбиваем текст на строки по 20 символов
                button = QPushButton(i)
                button.setObjectName(group)
                button.clicked.connect(
                    functools.partial(self.on_click_add_test, layout2=layout2, semestr=semestr))
                layout1.addWidget(button)
        except:
            # Получение информации об исключении
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def on_click_add_test(self, layout2, semestr):
        try:
            for i in reversed(range(layout2.count())):
                layout2.itemAt(i).widget().deleteLater()
            group = self.sender().objectName()
            lesson = self.sender().text()
            self.status_bar.set_lesson(lesson)
            self.current_lesson = lesson
            self.current_group = group
            self.student_ids = self.dict_semestr_lesson[semestr][group]["students"]
            self.tests = self.dict_semestr_lesson[semestr][group]["lessons"][lesson]
            for i in self.tests:
                wrapped_text = "\n".join(textwrap.wrap(i, width=20))  # разбиваем текст на строки по 20 символов
                button = QPushButton(wrapped_text)
                button.setObjectName(i)
                try:
                    button.clicked.connect(self.open_dialog)
                except:
                    # Получение информации об исключении
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    log_exception(exc_type, exc_value, exc_traceback)
                layout2.addWidget(button)
        except:
            # Получение информации об исключении
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def open_dialog(self):
        try:
            self.users_name_checkbox_layout = QVBoxLayout()
            button_name = self.sender().objectName()
            dialog = QDialog()
            dialog.setWindowTitle(button_name)
            dialog.setGeometry(400, 400, 350, 300)
            icon = QIcon('resources/favicon.ico')
            dialog.setWindowIcon(icon)

            main_layout = QGridLayout()
            scroll_area = QScrollArea()  # Создаем QScrollArea
            scroll_content = QWidget()  # Виджет для размещения чекбоксов
            scroll_content.setLayout(self.users_name_checkbox_layout)

            search_edit = QLineEdit(self)
            search_edit.setPlaceholderText("Поиск...")
            search_edit.textChanged.connect(functools.partial(self.filter_checkboxes, search_edit=search_edit))
            main_layout.addWidget(search_edit, 0, 0)

            scroll_area.setWidget(scroll_content)  # Устанавливаем виджет в QScrollArea
            scroll_area.setWidgetResizable(True)  # Делаем виджет изменяемым в размере

            main_layout.addWidget(scroll_area, 1, 0)  # Добавляем QScrollArea в макет

            self.test_url = self.tests[button_name]
            self.current_test_name = button_name
            self.status_bar.set_test(button_name)
            for _id in self.student_ids:
                checkbox = QCheckBox(self.students[_id])
                checkbox.setObjectName(_id)
                self.users_name_checkbox_layout.addWidget(checkbox)

            button_all = QPushButton("Отметить всех")
            button_all.clicked.connect(self.on_click_all_check)
            main_layout.addWidget(button_all, 2, 0)

            button_rdy = QPushButton("Пройти")
            button_rdy.clicked.connect(self.on_click_ready)
            main_layout.addWidget(button_rdy, 3, 0)

            button_stop = QPushButton("Прервать тест")
            button_stop.clicked.connect(self.stop_test)
            main_layout.addWidget(button_stop, 4, 0)

            dialog.setLayout(main_layout)
            dialog.exec_()
        except:
            # Получение информации об исключении
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def filter_checkboxes(self, search_edit):
        search_text = search_edit.text().lower()
        for i in range(self.users_name_checkbox_layout.count()):
            item = self.users_name_checkbox_layout.itemAt(i)
            if isinstance(item.widget(), QCheckBox):
                checkbox_text = item.widget().text().lower()
                item.widget().setVisible(search_text in checkbox_text)

    def stop_test(self):
        self.stop_flag = True
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
        else:
            self.warning("Тестирование не активно")

    def on_click_all_check(self):
        try:
            layout = self.users_name_checkbox_layout
            for i in range(layout.count()):
                layout.itemAt(i).widget().setChecked(True)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def on_click_ready(self):
        try:
            if self.thread is None or not self.thread.is_alive():
                layout = self.users_name_checkbox_layout
                answers_ = answers(self.current_lesson)

                checked_widgets = []

                for i in range(layout.count()):
                    widget = layout.itemAt(i).widget()
                    if isinstance(widget, QCheckBox) and widget.isChecked():
                        checked_widgets.append(widget.objectName())
                with open("resources/path.json") as json_file:
                    data_json = json.load(json_file)
                    path = data_json["screenshots"]
                self.stop_flag = False
                self.thread = threading.Thread(target=self.selenium_bot_test, args=(checked_widgets, answers_, path))
                self.thread.start()
            else:
                self.warning("Тест уже запущен")
        except FileNotFoundError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"Файл с ответами: {e.filename} не найден")
            log_exception(exc_type, exc_value, exc_traceback)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def selenium_bot_test(self, checked_widgets: list[str], answers_, path_screen):
        for id_ in checked_widgets:
            if self.stop_flag:
                break
            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
            fio = self.students[id_]
            url = self.test_url
            semestr = self.current_semestr
            lesson = self.current_lesson
            group = self.current_group
            test_name = self.current_test_name
            login = self.student_ids[id_]["login"]
            password = self.student_ids[id_]["password"]
            screenshots_path = f"{path_screen}/{semestr}/{group}/{lesson}/{test_name}/"
            screenshots_path = screenshots_path.replace("\\", "/")

            if not os.path.exists(screenshots_path):
                os.makedirs(screenshots_path)

            try:
                self.driver.get(url="https://dot.omgups.ru/login/index.php")

                username_field = self.driver.find_element(by=By.ID, value="username")
                password_field = self.driver.find_element(by=By.ID, value="password")
                login_field = self.driver.find_element(by=By.ID, value="loginbtn")

                username_field.send_keys(login)
                password_field.send_keys(password)

                login_field.click()

                self.driver.get(url=url)

                self.driver.execute_script("window.scrollTo(0, 1000);")

                self.driver.save_screenshot(f"{screenshots_path}/{fio}.{lesson}.начало.png")

                start_test = self.driver.find_element(by=By.CSS_SELECTOR,
                                                      value="button[type='submit'][class='btn btn-secondary']")

                start_test.click()

                time.sleep(2)

                try:
                    find_button = self.driver.find_element(by=By.ID, value="id_submitbutton")
                    find_button.click()
                except:
                    print("Все норм")

                time.sleep(10)

                switch = False

                if len(self.driver.window_handles) > 1:
                    switch = True
                    self.driver.switch_to.window(self.driver.window_handles[1])

                time.sleep(1)

                count = 0

                time.sleep(5)

                div_element = self.driver.find_element(by=By.CSS_SELECTOR,
                                                       value="div[class='qn_buttons clearfix multipages']")
                tag_elements = div_element.find_elements(by=By.TAG_NAME, value="a")

                len_tag_elements = len(tag_elements)

                if self.is_time:
                    time_end = int(self.choice_time) * 60
                else:
                    last_time = self.driver.find_element(by=By.ID, value="quiz-time-left")

                    time_format = "%H:%M:%S"

                    try:
                        time_obj = datetime.strptime(last_time.text, time_format)
                        time_in_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
                    except:
                        time_in_seconds = len_tag_elements * 60

                    time_sleep = (time_in_seconds * 0.333)

                    min_time = 300

                    max_time = time_sleep + random.choice([-180, 180])

                    if time_sleep > max_time:
                        time_sleep, max_time = max_time, time_sleep

                    time_end = random.randint(int(time_sleep), int(max_time))

                    if time_end < min_time:
                        time_end = 300 + random.randint(1, 180)

                time_end /= len_tag_elements

                while count <= len_tag_elements - 1:
                    try:
                        questions = self.driver.find_elements(by=By.CSS_SELECTOR, value="div[class='qtext']")
                        button_next = self.driver.find_element(by=By.CSS_SELECTOR,
                                                               value="input[type='submit'][name='next']")
                        time.sleep(time_end)
                        for question in questions:
                            count += 1
                            try:
                                que = answers_[question.text]
                            except:
                                que = approximate(answers_, question.text)
                            if que is not None:
                                for text in que:
                                    try:
                                        answer = self.driver.find_element(By.XPATH,
                                                                          f"//*[starts-with(normalize-space(), '{text}')]")
                                        answer.click()
                                    except:
                                        try:
                                            answer = self.driver.find_element(By.XPATH,
                                                                              f"//*[starts-with(normalize-space(), '{text.lower()}')]")
                                            answer.click()
                                        except:
                                            try:
                                                answer = self.driver.find_element(By.XPATH,
                                                                                  f"//*[starts-with(normalize-space(), '{text.strip()}')]")
                                                answer.click()
                                            except:
                                                try:
                                                    answer = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                                      value="input[type='text'][class='form-control d-inline']")
                                                    answer.send_keys(text)
                                                except:
                                                    try:
                                                        answers_page = self.driver.find_elements(By.CSS_SELECTOR,
                                                                                                 ".flex-fill.ml-1")

                                                        answer_texts = [answer.text for answer in answers_page]

                                                        most_que = find_most_similar_answer(text, answer_texts)

                                                        answer = self.driver.find_element(By.XPATH,
                                                                                          f"//*[starts-with(normalize-space(), '{most_que}')]")

                                                        answer.click()

                                                        fixed_pls = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                                             value="div[class='formulation clearfix']")

                                                        with open(screenshots_path + 'questions_failed.txt', 'a',
                                                                  encoding='utf-8') as file:
                                                            file.write(
                                                                f"\n{count} Не нашел ответ ({text}) на странице, но нашел примерно похожий и записал его ({most_que})")
                                                            file.write(f"\n{fixed_pls.text}")

                                                    except:
                                                        fixed_pls = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                                             value="div[class='formulation clearfix']")

                                                        with open(screenshots_path + 'questions_failed.txt', 'a',
                                                                  encoding='utf-8') as file:
                                                            file.write(f"\n{count} Не нашел ответ ({text}) на странице")
                                                            file.write(f"\n{fixed_pls.text}")
                            else:
                                fixed_pls = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                     value="div[class='formulation clearfix']")
                                with open(screenshots_path + 'questions_failed.txt', 'a',
                                          encoding='utf-8') as file:
                                    file.write(f"\n{count} ОТВЕТ НЕ НАЙДЕН")
                                    file.write(f"\n{fixed_pls.text}")
                        button_next.click()
                        time.sleep(1)
                    except:
                        if self.driver is None:
                            break
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        log_exception(exc_type, exc_value, exc_traceback)
                        continue

                try:
                    end_test = self.driver.find_element(By.XPATH, "//button[text()='Отправить всё и завершить тест']")
                    end_test.click()
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    log_exception(exc_type, exc_value, exc_traceback)

                wait = WebDriverWait(self.driver, 30)

                try:
                    confirmation_dialog = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                       "div[class='confirmation-dialogue']")))
                    time.sleep(5)
                    confirmation_dialog.click()
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    log_exception(exc_type, exc_value, exc_traceback)

                if switch:
                    self.driver.switch_to.window(self.driver.window_handles[0])

                self.driver.get(url=url)

                self.driver.execute_script("window.scrollTo(0, 1000);")

                self.driver.save_screenshot(f"{screenshots_path}/{fio}.{lesson}.конец.png")

                time.sleep(5)

                if self.ip:
                    change_ip()

                self.driver.quit()

            except:
                if self.driver is None:
                    break
                self.driver.save_screenshot(f"{screenshots_path}/{fio}.{lesson}.ошибка.png")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                log_exception(exc_type, exc_value, exc_traceback)
                continue
