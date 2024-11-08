from uuid import UUID

import pandas as pd
import uuid

# загрузка файла
df = pd.read_excel('words.xlsx')

# выбор нужных столбцов
data = df.loc[df['ФИО'] != 'ФИО', ['ФИО', 'login', 'password']]

# создание словаря
result = {}

list_fio = {}

for index, row in data.iterrows():
    myuuid: UUID = uuid.uuid4()
    fio = row['ФИО']
    list_fio[str(myuuid)] = fio
    login = row['login']
    password = row['password']
    result[str(myuuid)] = {'login': login, 'password': password}


print(result)