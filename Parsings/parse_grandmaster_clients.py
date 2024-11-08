import pandas as pd
import os
import psycopg2


# Модель клиента
class Client:
    def __init__(self, _id, full_name, group_name, login, password, phone, semester_id):
        self.id = _id
        self.full_name = full_name
        self.group_name = group_name
        self.login = login
        self.password = password
        self.phone = phone
        self.semester_id = semester_id

    def __repr__(self):
        return f"Client({self.full_name}, {self.id}, {self.login}, {self.password}, {self.phone}, {self.group_name}, {self.semester_id})"


def process_excel(file_path):
    # Извлекаем семестр из названия файла (например, 3 из "3 семестр.xlsx")
    semester_id = 7

    # Загружаем все листы Excel файла
    xls = pd.ExcelFile(file_path)
    clients = []

    for sheet_name in xls.sheet_names:
        # Извлекаем группу из названия листа
        group_name = sheet_name

        # Читаем данные с листа
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Проходим по строкам DataFrame и создаем объекты Client
        for _, row in df.iterrows():
            client = Client(
                _id=row['Шифр'],
                full_name=row['ФИО'],
                group_name=group_name,
                login=row['Логин'],
                password=row['Пароль'],
                phone=row['Телефон'],
                semester_id=semester_id
            )
            clients.append(client)

    return clients


def insert_clients_to_db(clients):
    # Установить соединение с базой данных PostgreSQL
    conn = psycopg2.connect(
        dbname="grandmaster",
        user="postgres",
        password="01122008elaman",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    # SQL запрос для вставки данных
    insert_query = """
    INSERT INTO public.clients (cipher, name, "groupName", "semesterId", "phoneNumber", login, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    # Выполняем запрос для каждого клиента
    for client in clients:
        try:
            cursor.execute(insert_query, (
                client.id, client.full_name, client.group_name, client.semester_id, client.phone, client.login,
                client.password))
        except:
            print("Проблемный", client)

    # Зафиксировать изменения в базе данных
    conn.commit()

    # Закрыть соединение
    cursor.close()
    conn.close()


# Пример использования
file_path = 'C:\\Users\\Elaman\\NodeProjects\\grandmaster\\студенты\\7 семестр.xlsx'
clients_list = process_excel(file_path)
insert_clients_to_db(clients_list)
