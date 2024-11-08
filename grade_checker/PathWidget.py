import json

from PyQt5.QtWidgets import QFileDialog, QPushButton, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QWidget

from Indicator import Indicator


class PathWidget(QWidget):
    def __init__(self, name, func_check, path_name):
        super().__init__()
        self.path_name = path_name
        self.name = name
        self.func_check = func_check
        self.indicator = Indicator()
        self.path_db = QLineEdit(self)
        self.label_errors = QLabel()
        self.main_layout = QGridLayout()
        self.up_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.up_layout, 0, 0)
        self.main_layout.addWidget(self.label_errors, 1, 0)
        self.init_ui()

    def init_ui(self):
        label = QLabel(self.name)
        self.path_db.setReadOnly(True)

        browse_button = QPushButton('Обзор', self)
        browse_button.clicked[bool].connect(self.choose_folder)

        self.up_layout.addWidget(label)
        self.up_layout.addWidget(self.path_db)
        self.up_layout.addWidget(browse_button)
        self.up_layout.addWidget(self.indicator)

        with open("resources/path.json") as json_file:
            data = json.load(json_file)
            path = data[self.path_name]

        if path is not None:
            res = self.func_check(path)
            if not res["Access"]:
                self.label_errors.setText("Нет доступа к папке")
                self.indicator.toggle_value(False)
            elif len(res["Errors"]) != 0:
                self.label_errors.setText("\n".join(res["Errors"]))
                self.indicator.toggle_value(False)
            else:
                self.label_errors.setText("")
                self.path_db.setText(path)
                self.indicator.toggle_value(True)

    def choose_folder(self):
        folder_dialog = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_dialog:
            self.path_db.setText(folder_dialog)
        else:
            folder_dialog = self.path_db.text()
        res = self.func_check(folder_dialog)
        if not res["Access"]:
            self.label_errors.setText("Нет доступа к папке")
            self.indicator.toggle_value(False)
        elif len(res["Errors"]) != 0:
            self.label_errors.setText("\n".join(res["Errors"]))
            self.indicator.toggle_value(False)
        else:
            self.label_errors.setText("")
            with open("resources/path.json", "r+") as json_file:
                data = json.load(json_file)
                data[self.path_name] = folder_dialog
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()
            self.indicator.toggle_value(True)
