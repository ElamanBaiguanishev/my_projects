import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar, QLabel, QHBoxLayout, QTabWidget

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.label1 = QLabel("Группа: Группа 1")
        self.label2 = QLabel("Предмет: Математика")
        self.label3 = QLabel("Тест: Тест 1")
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        self.setLayout(layout)

    def set_group(self, group):
        self.label1.setText(f"Группа: {group}")

    def set_subject(self, subject):
        self.label2.setText(f"Предмет: {subject}")

    def set_test(self, test):
        self.label3.setText(f"Тест: {test}")

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.tab_widget = QTabWidget()  # Ваш код создания QTabWidget
        self.main_layout.addWidget(self.tab_widget)

        self.status_widget = StatusWidget()
        self.status_bar = QStatusBar()
        self.status_bar.addWidget(self.status_widget)
        self.main_layout.addWidget(self.status_bar)

    def show_group(self, group):
        self.status_widget.set_group(group)

    def show_subject(self, subject):
        self.status_widget.set_subject(subject)

    def show_test(self, test):
        self.status_widget.set_test(test)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.setWindowTitle("Пример с множеством данных в строке состояния")
    ex.setGeometry(100, 100, 400, 200)
    ex.show()
    ex.show_group("Группа 1")
    ex.show_subject("Математика")
    ex.show_test("Тест 1")
    sys.exit(app.exec_())