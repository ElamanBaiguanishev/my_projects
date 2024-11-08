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
        cursor.execute('INSERT INTO data (id, text)  VALUES (?, ?)', (id_, "{}"))

        conn.commit()
    except Exception as e:
        print("init_db", e)


def get_data(id_: int) -> dict:
    try:
        cursor.execute('SELECT * FROM data WHERE id = ?', (id_,))
        record = cursor.fetchone()

        old_data = json.loads(record[1])

        conn.commit()
        return old_data
    except Exception as e:
        print("get_data", e)
        return {}


def replace_data(data_, id_: int) -> int:
    try:
        sql_query = f"UPDATE data SET text = ? WHERE id = ?"
        cursor.execute(sql_query, (json.dumps(data_), id_))

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        return len(list(data_.values())[0])
    except Exception as e:
        print("replace_data", e)
        return 0


def add_data(data_, id_: int) -> int:
    try:
        old_data = get_data(id_)

        new_data = {key: list(set(old_data.get(key, []) + data_.get(key, []))) for key in set(old_data) | set(data_)}

        replace_data(new_data, id_)
        try:
            len_old_data = len(list(old_data.values())[0])
        except:
            len_old_data = 0

        conn.commit()
        return len(list(new_data.values())[0]) - len_old_data
    except Exception as e:
        print("add_data", e)
        return 0


def clean_data(id_: int) -> int:
    try:
        old_data = get_data(id_)

        replace_data({list(old_data.keys())[0]: []}, id_)

        conn.commit()

        return len(list(old_data.values())[0])
    except Exception as e:
        print("clean_data", e)
        return 0
