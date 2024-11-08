import json
import re
import sys

from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QCheckBox, QLineEdit, QLayoutItem, QHBoxLayout, \
    QPushButton, QMessageBox, QProgressBar, QLabel

from WorkerThread import WorkerThread
from tools import log_exception


class Scroll(QWidget):
    def __init__(self, service):
        super().__init__()
        self.semester = None
        self.current_group = None

        self.worker_thread = WorkerThread(service)
        self.worker_thread.update_progress_signal.connect(self.update_progress)
        self.worker_thread.signal_error.connect(self.handle_error)
        self.worker_thread.choice_error.connect(self.choice_error)

        self.main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Поиск...")
        self.search_edit.textChanged.connect(self.filter_checkboxes)
        self.main_layout.addWidget(self.search_edit)

        self.buttons_layout = QHBoxLayout()

        record_book_button = QPushButton("Зачетка")
        debts = QPushButton("Долги")
        stop = QPushButton("Стоп")
        all_checks = QPushButton("Отметить всех")

        record_book_button.clicked.connect(self.pre_start)
        debts.clicked.connect(self.pre_start)
        stop.clicked.connect(self.stop_thread)
        all_checks.clicked.connect(self.on_click_all_check)

        self.buttons_layout.addWidget(record_book_button)
        self.buttons_layout.addWidget(debts)
        self.buttons_layout.addWidget(stop)
        self.buttons_layout.addWidget(all_checks)

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addLayout(self.buttons_layout)

        progress_bar_layout = QVBoxLayout()
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel("")
        progress_bar_layout.addWidget(self.progress_bar)
        progress_bar_layout.addWidget(self.progress_label)
        self.main_layout.addLayout(progress_bar_layout)

    def create_list(self, students, semester, group):
        self.current_group = group
        self.semester = int(re.findall(r'\d+', semester)[0])
        self.clear_layout(self.scroll_layout)
        for student, valid in students.items():
            checkbox = QCheckBox(student + " - " + valid, self.scroll_widget)
            checkbox.setObjectName(json.dumps([student, valid]))
            self.scroll_layout.addWidget(checkbox)

    def on_click_all_check(self):
        layout = self.scroll_layout
        for i in range(layout.count()):
            layout.itemAt(i).widget().setChecked(True)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QLayoutItem):
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())

    def filter_checkboxes(self):
        search_text = self.search_edit.text().lower()
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if isinstance(item.widget(), QCheckBox):
                checkbox_text = item.widget().text().lower()
                item.widget().setVisible(search_text in checkbox_text)

    def pre_start(self):
        try:
            if not self.worker_thread.isRunning():
                button_name = self.sender().text()
                layout = self.scroll_layout

                checked_widgets = []

                for i in range(layout.count()):
                    item = layout.itemAt(i).widget()
                    if isinstance(item, QCheckBox) and item.isChecked():
                        checked_widgets.append(item.objectName())

                quantity = len(checked_widgets)
                if quantity > 0:
                    with open("resources/path.json") as json_file:
                        data_json = json.load(json_file)
                        path = data_json["screenshots"]

                    self.worker_thread.is_running = True

                    self.progress_bar.setMaximum(quantity)

                    self.worker_thread.set_arguments(checked_widgets, path, button_name, self.semester,
                                                     self.current_group)
                    self.worker_thread.start()
                else:
                    self.handle_error("Выберите хотя бы 1 студента")
            else:
                print("Процесс запущен")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log_exception(exc_type, exc_value, exc_traceback)
            self.handle_error(str(e))

    def handle_error(self, str_):
        QMessageBox.warning(self, "Warning", str_)

    def choice_error(self, error_message):
        reply = QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка: {error_message}. Продолжить?',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.No:
            self.worker_thread.is_running = False
            self.worker_thread.is_cycle = False
        elif reply == QMessageBox.Yes:
            self.worker_thread.is_running = True
            self.worker_thread.is_cycle = False

    def stop_thread(self):
        if self.worker_thread.is_running:
            reply = QMessageBox.warning(self, 'Предупреждение', 'Остановить процесс?',
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.worker_thread.is_running = False
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Процесс не запущен')

    def update_progress(self, value, text):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"Обрабатываю {text}")
