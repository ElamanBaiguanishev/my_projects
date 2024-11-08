import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor
import win32gui
import win32con


class Overlay(QWidget):
    def __init__(self, hwnd):
        super().__init__()

        self.hwnd = hwnd

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(0, 0, 400, 300)  # Установите размер вашего оверлея
        self.move(100, 100)  # Установите начальную позицию оверлея

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Нарисуйте какие-то элементы на вашем оверлее
        painter.setBrush(QBrush(QColor(255, 0, 0, 128)))
        painter.drawRect(self.rect())


def main():
    hwnd = 395710  # Замените этот код на HWND вашей игры

    app = QApplication(sys.argv)

    # Создание оверлейного окна с помощью WinAPI
    overlay = Overlay(hwnd)
    overlay.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
