import sys
import time
import subprocess
import win32gui
import win32con
import win32api
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class OverlayWindow(QWidget):
    def __init__(self, target_hwnd):
        super().__init__()
        self.target_hwnd = target_hwnd
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        self.label = QLabel('Overlay Text', self)
        self.label.setFont(QFont('Arial', 20))
        self.label.setStyleSheet("color: black;")  # Черный цвет текста

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Получаем HWND окна оверлея
        overlay_hwnd = int(self.winId())
        print(f"Overlay HWND: {overlay_hwnd}")

        # Устанавливаем расширенный стиль окна оверлея
        ex_style = win32gui.GetWindowLong(overlay_hwnd, win32con.GWL_EXSTYLE)
        ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(overlay_hwnd, win32con.GWL_EXSTYLE, ex_style)

        # Устанавливаем прозрачность окна оверлея
        win32gui.SetLayeredWindowAttributes(overlay_hwnd, win32api.RGB(0, 0, 0), 0,
                                            win32con.LWA_COLORKEY)  # Прозрачный фон

    def update_overlay(self):
        # Обновляем содержимое оверлея
        pass


def find_window_partial(title):
    def enum_windows_callback(hwnd, results):
        if title in win32gui.GetWindowText(hwnd):
            results.append(hwnd)

    results = []
    win32gui.EnumWindows(enum_windows_callback, results)
    if results:
        return results[0]
    raise Exception(f"Window containing title '{title}' not found!")


if __name__ == '__main__':
    # Запускаем приложение
    process = subprocess.Popen(['notepad.exe'])  # Замените 'notepad.exe' на нужное вам приложение

    # Ждем, чтобы приложение запустилось и окно появилось
    time.sleep(5)  # Увеличьте время ожидания, если необходимо

    # Находим окно приложения
    hwnd = find_window_partial('Блокнот')  # Используйте часть заголовка для большей гибкости
    print(f"Target window HWND: {hwnd}")

    app = QApplication(sys.argv)
    overlay = OverlayWindow(hwnd)
    overlay.show()

    timer = QTimer()
    timer.timeout.connect(overlay.update_overlay)
    timer.start(1000)  # Обновляем каждую секунду

    sys.exit(app.exec_())
