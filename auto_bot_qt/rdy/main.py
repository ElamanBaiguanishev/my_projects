import functools
import sys
import textwrap
import traceback
import logging
from json import JSONDecodeError

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QTabWidget, QSizePolicy, QLabel, QGroupBox, \
    QVBoxLayout, QDialog, QCheckBox, QMessageBox, QProgressBar

from parsing import data, check_config
from rdy.parse_answers import answers
from rdy.script_bot import start
from tools import *


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
    def __init__(self):
        super().__init__()
        self.current_lesson = None
        self.students = None
        self.dict_semestr_lesson = None
        self.grid = None
        self.tests = None
        self.test = None
        self.users_name_checkbox_layout = None
        self.student_ids = None
        self.lessons = None
        self.current_semestr = None
        self.tab_widget = QTabWidget()
        self.main_layout = QGridLayout()
        self.init_ui()
        self.main_layout.addWidget(self.tab_widget)

    def init_ui(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(600, 200, 568, 500)
        self.setStyleSheet("background: #f7f7f7")
        icon = QIcon('resources/favicon.ico')
        self.setWindowIcon(icon)

        self.setStyleSheet(open("resources/styles.qss", "r").read())

        if not check_config():
            try:
                progress_dialog = ProgressDialog()
                progress_dialog.show()
                self.dict_semestr_lesson, self.students = data(True, progress_dialog.update_progress)
            except FileNotFoundError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"Файл по пути: {e.filename} не найден")
                log_exception(exc_type, exc_value, exc_traceback)
            except:
                # Получение информации об исключении
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                             f"Тип исключения:, {exc_type}\n"
                             f"Сообщение об ошибке:, {exc_value}")
                log_exception(exc_type, exc_value, exc_traceback)
        else:
            reply = QMessageBox.question(self, 'Добро пожаловать',
                                         'Обновить список семестров?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                try:
                    progress_dialog = ProgressDialog()
                    progress_dialog.show()
                    self.dict_semestr_lesson, self.students = data(True, progress_dialog.update_progress)
                except FileNotFoundError as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.warning(f"Файл по пути: {e.filename} не найден")
                    log_exception(exc_type, exc_value, exc_traceback)
                except:
                    # Получение информации об исключении
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                                 f"Тип исключения:, {exc_type}\n"
                                 f"Сообщение об ошибке:, {exc_value}")
                    log_exception(exc_type, exc_value, exc_traceback)
            elif reply == QMessageBox.No:
                try:
                    self.dict_semestr_lesson, self.students = data(False)  # Передаем функцию update_progress
                except JSONDecodeError as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.warning(f"Файл конфига для загрузки данных поврежден \n{e}")
                    log_exception(exc_type, exc_value, exc_traceback)
                except FileNotFoundError as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.warning(f"Файл конфига не найден \n{e}")
                    log_exception(exc_type, exc_value, exc_traceback)
                except:
                    # Получение информации об исключении
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                                 f"Тип исключения:, {exc_type}\n"
                                 f"Сообщение об ошибке:, {exc_value}")
                    log_exception(exc_type, exc_value, exc_traceback)
            else:
                sys.exit()

        self.setLayout(self.main_layout)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.create_tabs()

    def warning(self, text: str):
        QMessageBox.warning(self, "Warning", text)

    def tab_changed(self, index):
        try:
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
            semestr = self.sender().objectName()
            self.current_semestr = semestr
            group = self.sender().text()
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
            self.current_lesson = lesson
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
                    traceback_details = traceback.format_exc()

                    # Вывод подробной информации об ошибке
                    print("Произошла ошибка:")
                    print("Тип исключения:", exc_type)
                    print("Сообщение об ошибке:", exc_value)
                    print("Подробности ошибки:")
                    print(traceback_details)
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
            # self.current_lesson = button_name
            dialog = QDialog()
            dialog.setWindowTitle(button_name)
            dialog.setGeometry(400, 400, 350, 50)
            icon = QIcon('resources/favicon.ico')
            dialog.setWindowIcon(icon)

            main_layout = QGridLayout()
            main_layout.addLayout(self.users_name_checkbox_layout, 0, 0)
            self.test = self.tests[button_name]
            for _id in self.student_ids:
                checkbox = QCheckBox(self.students[_id])
                checkbox.setObjectName(_id)
                self.users_name_checkbox_layout.addWidget(checkbox)

            button_all = QPushButton("Отметить всех")
            button_all.clicked.connect(self.on_click_all_check)
            main_layout.addWidget(button_all)

            button_rdy = QPushButton("Пройти")
            button_rdy.clicked.connect(self.on_click_ready)
            main_layout.addWidget(button_rdy)

            dialog.setLayout(main_layout)
            dialog.exec_()
        except:
            # Получение информации об исключении
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.warning(f"К сожалению, возникла непредвиденная ошибка\n"
                         f"Тип исключения:, {exc_type}\n"
                         f"Сообщение об ошибке:, {exc_value}")
            log_exception(exc_type, exc_value, exc_traceback)

    def on_click_all_check(self):
        try:
            layout = self.users_name_checkbox_layout
            for i in range(layout.count()):
                layout.itemAt(i).widget().setChecked(True)
        except Exception as e:
            print(e)

    def on_click_ready(self):
        try:
            layout = self.users_name_checkbox_layout
            answers_ = answers(self.current_lesson)
            print(answers_)
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget.isChecked():
                    print(widget.objectName())
                    print(self.test)
                    print(self.current_lesson)
                    start(self.students[widget.objectName()], answers_,
                          self.student_ids[widget.objectName()]["login"],
                          self.student_ids[widget.objectName()]["password"],
                          self.test)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    log_filename = create_log_file()
    sys.excepthook = log_exception
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
