import json
import re


# Функция для определения режима карты
def map_mode(map_: str) -> str:
    match = re.search(r'\((\d+)\)', map_).group(1)

    if match == '2':
        return "1x1"
    if match == '4':
        return "2x2"
    if match == '6':
        return "3x3"
    if match == '8':
        return "4x4"

    return match


# Чтение данных из JSON-файла
with open('allMaps.json', encoding='utf-8') as mapsJson:
    existing_data = json.load(mapsJson)

# Генерация SQL-запросов INSERT
sql_queries = []
for map_id, (path, name) in enumerate(existing_data.items(), start=1):
    # Заменяем каждый апостроф на двойной апостроф внутри строки
    name = name.replace("'", "''")
    sql_query = f"INSERT INTO public.maps (id, name, map_mode, icon_path, description, author, \"order\") VALUES ({map_id}, '{name}', '{map_mode(name)}', '{path}', 'Описание', 'dowss', 1);"
    sql_queries.append(sql_query)

# Запись SQL-запросов в файл или выполнение их напрямую в PostgreSQL
with open('insert_queries.sql', 'w', encoding='utf-8') as sql_file:
    sql_file.write("\n".join(sql_queries))
