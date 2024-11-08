import json
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QPushButton

from ct import main_ct
from parsing import data


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(600, 200, 568, 500)
        self.setStyleSheet("background: #f7f7f7")
        icon = QIcon('resources/excel.ico')
        self.data = data()
        self.setWindowIcon(icon)

        self.main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        for i in self.data:
            button = QPushButton(str(i))
            button.setObjectName(json.dumps(i))
            button.clicked.connect(self.pre_start)
            self.scroll_layout.addWidget(button)

        self.main_layout.addWidget(self.scroll_area)

        self.show()

    def pre_start(self):
        try:
            json_valid = json.loads(self.sender().objectName())
            f = json_valid['f']
            i = json_valid['i']
            o = json_valid['o']
            group = json_valid['group']
            adapter = json_valid['adapter']
            login = json_valid['login']
            password = json_valid['password']
            url = json_valid['url']

            result = {
                "f": f,
                "i": i,
                "o": o,
                "group": group,
                "adapter": adapter,
                "login": login,
                "password": password,
                "url": url
            }

            with open("data_ct.json", 'w', encoding='utf-8') as file:
                json.dump(result, file, indent=4, ensure_ascii=False)
            self.hide()
            main_ct()
        except:
            self.show()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An exception occurred: {e}")
