import random
import sys
import textwrap

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QGridLayout, QCheckBox, \
    QSizePolicy

from parsing import dict_semestr_lesson, students
from rdy.script_bot import start


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(600, 200, 400, 300)
        icon = QIcon('resources/favicon.ico')
        self.student_ids = None
        self.lessons = None
        self.current_lesson = None
        self.setWindowIcon(icon)
        self.setStyleSheet("background: #f7f7f7")
        self.setAutoFillBackground(True)
        self.main_layout = QGridLayout()
        self.up_layout = QGridLayout()
        self.empty_widget = QWidget()
        self.empty_widget1 = QWidget()
        self.down_layout = QGridLayout()
        self.semestrs()
        self.right_layout = QGridLayout()
        self.right_layout.addWidget(self.empty_widget)
        self.down_layout.addWidget(self.empty_widget1)
        self.up_layout.addLayout(self.right_layout, 0, 1)
        self.main_layout.addLayout(self.up_layout, 0, 1)
        self.main_layout.addLayout(self.down_layout, 1, 1)
        self.setLayout(self.main_layout)
        self.users_name_checkbox_layout = None

    def semestrs(self):
        left_layout = QVBoxLayout()  # Макет для кнопок слева
        for i in range(6):  # Добавляю 6 кнопок
            button = QPushButton(f"Семестр {i + 1}")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(self.on_click_add_group)
            left_layout.addWidget(button)
        self.up_layout.addLayout(left_layout, 0, 0)

    def on_click_add_group(self):
        try:
            for i in reversed(range(self.right_layout.count())):
                self.right_layout.itemAt(i).widget().deleteLater()
            button_name = str(self.sender().text())
            lessons = dict_semestr_lesson[button_name]
            row = 0
            col = 0
            for i in lessons:
                button = QPushButton(i)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.clicked.connect(self.on_click_add_lesson)
                button.setObjectName(button_name)
                self.right_layout.addWidget(button, row, col)
                col += 1
                if col == 2:
                    row += 1
                    col = 0
        except Exception as e:
            print(e)

    def on_click_add_lesson(self):
        for i in reversed(range(self.down_layout.count())):
            self.down_layout.itemAt(i).widget().deleteLater()
        semestr = self.sender().objectName()
        button_name = self.sender().text()
        row = 0
        col = 0
        self.student_ids = dict_semestr_lesson[semestr][button_name]["students"]
        self.lessons = dict_semestr_lesson[semestr][button_name]["lessons"]
        for i in self.lessons:
            wrapped_text = "\n".join(textwrap.wrap(i, width=20))  # разбиваем текст на строки по 20 символов
            button = QPushButton(wrapped_text)
            button.setObjectName(i)
            try:
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.clicked.connect(self.open_dialog1)
            except Exception as e:
                print(e)
            self.down_layout.addWidget(button, row, col)
            col += 1
            if col == 3:
                row += 1
                col = 0

    def open_dialog1(self):
        try:
            self.users_name_checkbox_layout = QVBoxLayout()
            button_name = self.sender().objectName()
            dialog = QDialog()
            dialog.setWindowTitle(button_name)
            dialog.setGeometry(1000, 200, 200, 200)
            icon = QIcon('resources/favicon.ico')
            dialog.setWindowIcon(icon)

            main_layout = QGridLayout()
            main_layout.addLayout(self.users_name_checkbox_layout, 0, 0)
            self.current_lesson = self.lessons[button_name]
            for _id in self.student_ids:
                checkbox = QCheckBox(students[_id])
                checkbox.setObjectName(_id)
                self.users_name_checkbox_layout.addWidget(checkbox)

            button = QPushButton("Пройти")
            button.clicked.connect(self.on_click_ready)
            main_layout.addWidget(button)

            dialog.setLayout(main_layout)
            dialog.exec_()
        except Exception as e:
            print(e)

    def on_click_ready(self):
        try:
            layout = self.users_name_checkbox_layout
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget.isChecked():
                    start(self.student_ids[widget.objectName()]["login"],
                          self.student_ids[widget.objectName()]["password"])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.setStyleSheet(open("resources/styles.qss", "r").read())
    sys.exit(app.exec_())
