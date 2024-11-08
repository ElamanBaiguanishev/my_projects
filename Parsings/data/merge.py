import os
import json
import re

from data import data

for login in data:
    with open(f"{login}.json", encoding='utf-8') as json_file:
        buffer: dict[str, dict] = json.load(json_file)
        new_buff = {}
        for fio, info in buffer.items():
            new_buff[info["user_id"]] = {
                "ФИО": fio,
                "group": info["Группа"]
            }
            group_filename = re.sub(r'[^A-Za-zА-Яа-я]', '', info["Группа"])
            group_filename += ".json"
            # Проверяем, существует ли файл с именем info["Группа"]
            if not os.path.exists(group_filename):
                # Если файла нет, создаем новый с пустым словарем
                with open(group_filename, 'w', encoding='utf-8') as group_file:
                    json.dump({}, group_file)

            # Загружаем существующие данные из файла
        with open(group_filename, 'r', encoding='utf-8') as group_file:
            existing_data = json.load(group_file)

        # Добавляем новые данные
        existing_data.update(new_buff)

        with open(group_filename, 'w', encoding='utf-8') as group_file:
            json.dump(existing_data, group_file, ensure_ascii=False)
