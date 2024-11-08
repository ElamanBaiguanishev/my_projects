from PyQt5.QtWidgets import QWidget, QPushButton, QButtonGroup, QGridLayout


class Buttons(QWidget):
    def __init__(self, button_names):
        super().__init__()

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        layout = QGridLayout(self)
        row = 0
        col = 0
        for name in button_names:
            button = QPushButton(name)
            button.setFixedSize(55, 25)
            button.setCheckable(True)
            self.button_group.addButton(button)
            layout.addWidget(button, row, col)
            col += 1
            if col == 2:
                row += 1
                col = 0
