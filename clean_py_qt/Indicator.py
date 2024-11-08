import sys
from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtGui import QColor


class Indicator(QFrame):
    def __init__(self):
        super().__init__()
        self.value = False
        self.col = QColor(0, 0, 0)
        self.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
        self.set_color()
        self.setFixedSize(20, 20)

    def set_color(self):
        if self.value is False:
            self.col.setRgb(255, 0, 0)  # Красный
        elif self.value is True:
            self.col.setRgb(0, 255, 0)  # Зеленый

        self.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

    def toggle_value(self, value):
        self.value = value
        self.set_color()
