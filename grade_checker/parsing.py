import json
import os
import re
import sys

import pandas as pd

from tools import group_en_to_ru

config_path = "resources/db.json"


def check_config() -> bool:
    try:
        if os.path.getsize(config_path) == 0:
            return False
        else:
            return True
    except FileNotFoundError:
        return False


def format_student_string(student_str):
    parts = student_str.split('_')
    len_parts = len(parts)
    if len_parts < 2:
        parts = student_str.split('-')
    try:
        part1 = re.sub(r'[^\w\s]+|[\d]+', r'', parts[1]).strip()
        part2 = parts[2]
        if len_parts > 3:
            return f"{group_en_to_ru[part1]}-{part2}-{parts[3]}"
        else:
            if len(parts[2]) < 6 or len(parts[2]) > 6:
                return f"{group_en_to_ru[part1]}-{part2}"
            else:
                return f"{group_en_to_ru[part1]}-{part2[:2]}-{part2[2:]}"
    except:
        return "Неизвестный формат, обратитесь к разработчику"


def data(command, progress_callback=None) -> dict:
    if command:
        with open("resources/path.json") as json_file:
            data_json = json.load(json_file)
            path = data_json["db"]
        dirs = os.listdir(path)
        total_dirs = len(dirs)
        result = {}
        try:
            for index, dir_ in enumerate(dirs):
                progress_value = (index + 1) / total_dirs * 100
                progress_callback(progress_value)
                result[dir_] = {}
                for folder_group in os.listdir(os.path.join(path, dir_)):
                    result[dir_][folder_group] = {}

                    key_counters = {}

                    for _, row in pd.read_excel(os.path.join(path, dir_, folder_group) + "/Студенты.xlsx", header=None,
                                                skiprows=1).iterrows():
                        original_key = str(row[0]).strip()
                        key = original_key

                        if key in key_counters:
                            key_counters[key] += 1
                            key = f"{original_key}_{key_counters[key]}"
                        else:
                            key_counters[key] = 1

                        result[dir_][folder_group][key] = format_student_string(str(row[1]).strip().lower())
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)
            print(os.path.join(path, dir_, folder_group) + "/Студенты.xlsx")

        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        return result
    else:
        with open(config_path, encoding='utf-8') as file:
            result = json.load(file)
        return result
