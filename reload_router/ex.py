import os
import json

# Создаем пустой словарь для хранения данных из JSON файлов
combined_data = {}

# Получаем список файлов в папке
folder_path = 'C:/Users/Elaman/PycharmProjects/Parsings/group'

file_names = [file for file in os.listdir(folder_path) if file.endswith('.json')]

# Читаем данные из каждого файла и добавляем их в общий словарь
for file_name in file_names:
    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
        data = json.load(file)
        combined_data.update(data)

# Записываем объединенные данные в новый JSON файл
with open('combined_file.json', 'w', encoding='utf-8') as file:
    json.dump(combined_data, file)
