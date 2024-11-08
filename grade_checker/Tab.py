from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox

from Buttons import Buttons
from Scroll import Scroll


class Tab(QWidget):
    def __init__(self, semester, data, service):
        super().__init__()
        self.data = data
        self.lesson = None
        self.group = None
        self.semester = semester

        self.main_layout = QGridLayout()

        self.tab_group = QGroupBox("Группы")
        self.tab_group_layout = QGridLayout()
        self.tab_group.setLayout(self.tab_group_layout)
        self.main_layout.addWidget(self.tab_group, 0, 0)

        self.scroll_area = Scroll(service)
        self.main_layout.addWidget(self.scroll_area, 0, 1)

        self.setLayout(self.main_layout)
        self.create_groups()

    def create_groups(self):
        buttons = Buttons(self.data[self.semester])
        buttons.button_group.buttonClicked.connect(self.create_students)
        self.tab_group_layout.addWidget(buttons, 0, 0)

    def create_students(self, button):
        self.group = button.text()
        self.scroll_area.create_list(self.data[self.semester][self.group], self.semester, self.group)
