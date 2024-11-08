import os

import pandas as pd

import shutil

main_folder = "db_new/"
for filename in os.listdir(main_folder):
    file_path = os.path.join(main_folder, filename)
    shutil.rmtree(file_path)

xls = pd.ExcelFile('Прайс.xlsx')

dfs = {}

sheet_names = xls.sheet_names

for sheet_name in sheet_names:
    dfs[sheet_name] = pd.read_excel(xls, sheet_name, skiprows=1)

count = 0

for sheet_name, df in dfs.items():
    count = count + 1

    result: dict[str, list | dict[str, list]] = {}

    current_folder = main_folder + f"Семестр {count}" + '/'

    os.makedirs(current_folder)

    for index, row in df.iterrows():
        try:
            if "/" in row[0]:
                split = row[0].split("/")
                print(split)
                for row1 in split:
                    if row1 not in result:
                        result[row1] = {"lessons": [], "students": {"fio's": [], "logins": [], "passwords": []}}
                    result[row1]["lessons"].append(row[1])
                    if isinstance(row[2], str):
                        result[row1]["students"]["fio's"].append(row[2])
                        result[row1]["students"]["logins"].append(row[3])
                        result[row1]["students"]["passwords"].append(row[4])
            else:
                if row[0] not in result:
                    result[row[0]] = {"lessons": [], "students": {"fio's": [], "logins": [], "passwords": []}}
                result[row[0]]["lessons"].append(row[1])
                if isinstance(row[2], str):
                    result[row[0]]["students"]["fio's"].append(row[2])
                    result[row[0]]["students"]["logins"].append(row[3])
                    result[row[0]]["students"]["passwords"].append(row[4])
        except Exception as e:
            print(e)
    print(result)

    for key, value in result.items():
        try:
            os.makedirs(current_folder + key)
            # создаем датафрейм из списка данных
            # df = pd.DataFrame(value["lessons"], columns=['Предмет'])
            # # сохраняем датафрейм в Excel-файл
            # df['Ссылка'] = ''
            # df.to_excel(current_folder + key + '/lessons.xlsx', index=False)
            # import pandas as pd
            #
            # # Создаем список с названиями листов
            # sheet_names = ['Sheet1', 'Sheet2', 'Sheet3']

            # Создаем пустой эксель файл
            writer = pd.ExcelWriter(current_folder + key + '/lessons.xlsx', engine='xlsxwriter')

            # Проходим по списку с названиями листов и создаем на каждом из них два дата фрейма
            for sheet in value["lessons"]:
                # Создаем дата фреймы
                df2 = pd.DataFrame({'Тест': ["Промежуточный", "Промежуточный1", "Итоговый"], 'Ссылка': ['www.example.com', 'www.google.com', 'www.github.com']})

                # Получаем название листа и обрезаем его до 31 символа
                sheet_name = sheet[:31]

                # Записываем дата фреймы на листы с обрезанным названием
                df2.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0, index=False)

            # Сохраняем и закрываем эксель файл
            writer.close()

            df1 = pd.DataFrame()
            df1['ФИО'] = value["students"]["fio's"]
            df1['login'] = value["students"]["logins"]
            df1['password'] = value["students"]["passwords"]
            df1.to_excel(current_folder + key + '/students.xlsx', index=False)
        except Exception as e:
            print(key, value["lessons"])
            print(e)
