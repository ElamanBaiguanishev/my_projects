from PyQt5.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.group = ""
        self.lesson = ""
        self.test = ""
        self.showMessage(f"Группа: {self.group} Предмет: {self.lesson} Тест: {self.test}")

    def clear(self):
        self.showMessage("Группа: Предмет: Тест: ")

    def set_group(self, group):
        self.group = group
        self.showMessage(f"Группа: {self.group} Предмет: Тест: ")

    def set_lesson(self, lesson):
        self.lesson = lesson
        self.showMessage(f"Группа: {self.group} Предмет: {self.lesson} Тест: ")

    def set_test(self, test):
        self.test = test
        self.showMessage(f"Группа: {self.group} Предмет: {self.lesson} Тест: {self.test}")
