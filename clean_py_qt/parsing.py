import json
import os
import pandas as pd
import uuid

config_path = "resources/db.json"

def check_config() -> bool:
    try:
        if os.path.getsize(config_path) == 0:
            return False
        else:
            return True
    except FileNotFoundError:
        return False


def data(command, progress_callback=None) -> tuple[dict, dict]:
    if command:
        with open("resources/path.json") as json_file:
            data_json = json.load(json_file)
            path = data_json["db"]
        dirs = os.listdir(path)
        students = {}

        def generate(path_group, item):
            if item == "students":
                df = pd.read_excel(path_group + "\\Студенты.xlsx", header=None, skiprows=1, usecols=[0, 1, 2])
                data_dict = {}

                for _, row in df.iterrows():
                    my_uuid: str = str(uuid.uuid4())
                    key = my_uuid
                    students[my_uuid] = row[0]
                    value_dict = {"login": row[1], "password": row[2]}
                    if key in data_dict:
                        data_dict[key].update(value_dict)
                    else:
                        data_dict[key] = value_dict

                return data_dict
            elif item == "lessons":
                excel_file = pd.ExcelFile(path_group + "\\Предметы.xlsx")
                sheet_names = excel_file.sheet_names
                return {
                    sheet_name: {
                        row[0]: row[1]
                        for _, row in pd.read_excel(excel_file, sheet_name).iterrows()
                    }
                    for sheet_name in sheet_names
                }

        dict_semestr_lesson = {}
        total_dirs = len(dirs)

        for index, dir_ in enumerate(dirs):
            progress_value = (index + 1) / total_dirs * 100
            progress_callback(progress_value)

            dict_semestr_lesson[dir_] = {
                folder_group: {
                    item: generate(os.path.join(path, dir_, folder_group), item)
                    for item in ["lessons", "students"]
                }
                for folder_group in os.listdir(os.path.join(path, dir_))
            }

        your_tuple = dict_semestr_lesson, students

        with open(config_path, 'w') as file:
            json.dump(your_tuple, file, indent=4, ensure_ascii=False)

        return your_tuple
    else:
        with open(config_path, 'r') as file:
            datas = json.load(file)
        return datas
