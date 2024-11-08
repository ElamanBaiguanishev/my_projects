import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QScrollArea, QCheckBox, QLineEdit

from kek import generate_random_string


class CheckBoxListWidget(QWidget):
    def __init__(self, parent=None):
        super(CheckBoxListWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        # Создаем QScrollArea
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Создаем виджет, который будет содержать список QCheckBox
        self.scroll_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        # Создаем вертикальный layout для виджета со списком QCheckBox
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        # Создаем поисковик
        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Поиск...")
        self.search_edit.textChanged.connect(self.filter_checkboxes)
        self.layout.addWidget(self.search_edit)

        # Добавляем несколько QCheckBox в список
        for i in range(40):
            checkbox = QCheckBox(generate_random_string(), self.scroll_widget)
            self.scroll_layout.addWidget(checkbox)

        # Добавляем QScrollArea в основной layout
        self.layout.addWidget(self.scroll_area)

    def filter_checkboxes(self):
        # Функция для фильтрации и отображения только тех QCheckBox, которые соответствуют тексту поиска
        search_text = self.search_edit.text().lower()
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if isinstance(item.widget(), QCheckBox):
                checkbox_text = item.widget().text().lower()
                item.widget().setVisible(search_text in checkbox_text)


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        self.layout = QVBoxLayout(self)

        # Создаем QGroupBox
        self.group_box = QGroupBox("Тест", self)

        # Создаем экземпляр CheckBoxListWidget и добавляем его в QGroupBox
        self.checkbox_list_widget = CheckBoxListWidget(self.group_box)
        self.group_box_layout = QVBoxLayout(self.group_box)
        self.group_box_layout.addWidget(self.checkbox_list_widget)

        # Добавляем QGroupBox в основной layout
        self.layout.addWidget(self.group_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
