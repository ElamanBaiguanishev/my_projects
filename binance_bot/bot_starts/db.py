import json
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY,
        text TEXT
    )
''')


def init_db(id_: int):
    try:
        cursor.execute('INSERT INTO data (id, text)  VALUES (?, ?)', (id_, "[]"))

        conn.commit()
    except Exception as e:
        print("init_db", e)


def get_data(id_: int) -> list:
    try:
        cursor.execute('SELECT * FROM data WHERE id = ?', (id_,))
        record = cursor.fetchone()

        data_list = json.loads(record[1])

        conn.commit()
        return data_list
    except Exception as e:
        print("get_data", e)
        return []


def replace_data(data_, id_: int) -> int:
    try:
        sql_query = f"UPDATE data SET text = ? WHERE id = ?"

        cursor.execute(sql_query, (json.dumps(data_), id_))

        # Сохраняем изменения и закрываем соединение
        conn.commit()

        return len(data_)
    except Exception as e:
        print("replace_data", e)
        return 0


def add_data(data_, id_: int) -> int:
    try:
        old_data = get_data(id_)

        new_data = set(old_data + data_)

        replace_data(list(new_data), id_)

        conn.commit()

        return len(new_data) - len(old_data)
    except Exception as e:
        print("add_data", e)
        return 0


def clean_data(id_: int) -> int:
    try:
        old_data = get_data(id_)

        replace_data([], id_)

        conn.commit()

        return len(old_data)
    except Exception as e:
        print("clean_data", e)
        return 0
