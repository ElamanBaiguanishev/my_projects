import json
import os
import pandas as pd
import uuid

config_path = "resources/config.json"


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
        path = "db/"
        dirs = os.listdir(path)
        students = {}

        def generate(item):
            file_ = os.path.splitext(os.path.basename(item))[0]
            if file_ == "students":
                df = pd.read_excel(item, header=None, skiprows=1, usecols=[0, 1, 2])
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
            elif file_ == "lessons":
                try:
                    excel_file = pd.ExcelFile(item)
                    sheet_names = excel_file.sheet_names
                    return {
                        sheet_name: {
                            row[0]: row[1]
                            for _, row in pd.read_excel(excel_file, sheet_name).iterrows()
                        }
                        for sheet_name in sheet_names
                    }
                except Exception as e:
                    print(e)
                    print(item)

        dict_semestr_lesson = {}
        total_dirs = len(dirs)

        for index, dir_ in enumerate(dirs):
            progress_value = (index + 1) / total_dirs * 100
            progress_callback(progress_value)

            dict_semestr_lesson[dir_] = {
                folder_group: {
                    item: generate(os.path.join(path, dir_, folder_group, f"{item}.xlsx"))
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
