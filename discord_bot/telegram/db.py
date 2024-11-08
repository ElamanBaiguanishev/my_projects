# import json
# import sqlite3
#
#
# def init_db(id_: int):
#     try:
#         conn = sqlite3.connect('data.db')
#         cursor = conn.cursor()
#
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS data (
#                 id INTEGER PRIMARY KEY,
#                 text TEXT
#             )
#         ''')
#
#         cursor.execute('INSERT INTO data (id, text)  VALUES (?, ?)', (id_, "[]"))
#
#         conn.commit()
#         conn.close()
#     except Exception as e:
#         print(e)
#
#
# def get_data(id_: int) -> list:
#     try:
#         conn = sqlite3.connect('data.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM data WHERE id = ?', (id_,))
#         record = cursor.fetchone()
#
#         old_data = json.loads(record[1])
#
#         conn.commit()
#         conn.close()
#         return old_data
#     except Exception as e:
#         print(e)
#         return []
#
#
# def replace_data(data_, id_: int) -> int:
#     # Открываем соединение с базой данных
#     try:
#         conn = sqlite3.connect('data.db')
#         cursor = conn.cursor()
#
#         # Создаем таблицу, если она не существует
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS data (
#                 id INTEGER PRIMARY KEY,
#                 text TEXT
#             )
#         ''')
#
#         # Вставляем данные в таблицу
#         sql_query = f"UPDATE data SET text = ? WHERE id = ?"
#         cursor.execute(sql_query, (json.dumps(data_), id_))
#
#         # Сохраняем изменения и закрываем соединение
#         conn.commit()
#         conn.close()
#         return len(data_)
#     except Exception as e:
#         print(e)
#         return 0
#
#
# def add_data(data_, id_: int) -> int:
#     try:
#         conn = sqlite3.connect('data.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM data WHERE id = ?', (id_,))
#         record = cursor.fetchone()
#
#         old_data = json.loads(record[1])
#
#         new_data = set(old_data + data_)
#
#         replace_data(list(new_data), id_)
#
#         conn.commit()
#         conn.close()
#         return len(new_data) - len(old_data)
#     except Exception as e:
#         print(e)
#         return 0
#
#
# def clean_data(id_: int) -> int:
#     try:
#         conn = sqlite3.connect('data.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM data WHERE id = ?', (id_,))
#         record = cursor.fetchone()
#         old_data = json.loads(record[1])
#         replace_data([], id_)
#         conn.commit()
#         conn.close()
#         return len(old_data)
#     except Exception as e:
#         print(e)
#         return 0
