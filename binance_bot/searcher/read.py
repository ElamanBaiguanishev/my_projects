import json
import sqlite3

# Открываем соединение с базой данных
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Выполняем запрос к базе данных для получения записи с определенным id
sqlite_select_query = """SELECT * from data"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()


# Проверяем, что запись существует
# print(records)
for i in records:
    print(i)

# Закрываем соединение
conn.close()
