import os
import json


def count_keys_in_json_folder(folder_path):
    total_keys = []

    # Перебор файлов в папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            # Чтение JSON-файла
            with open(file_path, encoding='utf-8') as json_file:
                data: dict = json.load(json_file)

            # Подсчет ключей в JSON-объекте

            for i_ in data:
                total_keys.append(int(i_))

            # if isinstance(data, dict):
            #
            #     total_keys.append(data)

    return total_keys


folder_path = 'C:/Users/Elaman/PycharmProjects/Parsings/group'
total_keys_count = count_keys_in_json_folder(folder_path)

print(len(total_keys_count))
