import requests
import pandas as pd


def parse_excel(file_path: str):
    # Чтение всех листов Excel файла
    excel_data = pd.read_excel(file_path, sheet_name=None)

    parsed_data = []

    # Обработка каждого листа (каждой группы)
    for group_name, sheet_data in excel_data.items():
        # Получение заголовков колонок (начиная с 2-й колонки — это типы заданий)
        task_types = sheet_data.columns[1:]  # Пропускаем первую колонку (предмет)

        for index, row in sheet_data.iterrows():
            subject = row[0]  # Название предмета

            # Проход по каждому типу задания и его цене
            for task_type in task_types:
                price = row[task_type]

                # Если цена не пуста и больше 0, добавляем в список
                if pd.notna(price) and price > 0:
                    parsed_data.append({
                        'group': group_name,
                        'subject': subject,
                        'task_type': task_type,
                        'price': price,
                        'semesterId': 3  # Пример ID семестра, можно передавать динамически
                    })

    return parsed_data


# Пример использования:
file_path = 'C:\\Users\\Elaman\\NodeProjects\\grandmaster\\прайс лист\\3 семестр.xlsx'  # Путь к файлу
tasks = parse_excel(file_path)

# Адрес вашего API для создания нескольких задач
url = "http://localhost:3000/api/tasks/many"  # Замените на ваш реальный URL

# Отправка POST-запроса
response = requests.post(url, json=tasks)

# Проверка статуса ответа
if response.status_code == 201:
    print("Данные успешно отправлены!")
    print(response.json())  # Выводим ответ от сервера
else:
    print(f"Ошибка при отправке данных: {response.status_code}")
    print(response.text)
