import pandas as pd
import json

# Чтение данных из JSON-файла
with open('C:/Users/Elaman/PycharmProjects/reload_router/combined_file.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Преобразование данных JSON в DataFrame
df_json = pd.DataFrame.from_dict(json_data, orient='index')
df_json.reset_index(inplace=True)
df_json.rename(columns={'index': 'ID', 'ФИО': 'FullName', 'group': 'Group'}, inplace=True)

# Загрузка списка ФИО из Excel
excel_path = 'C:/Users/Elaman/PycharmProjects/Parsings/1 курс.xlsx'
df_excel = pd.read_excel(excel_path)

# Объединение данных по ФИО
df_merged = pd.merge(df_excel, df_json, left_on='ФИО', right_on='FullName', how='left')

# Сохранение результата в новый Excel-файл
output_path = 'result.xlsx'
df_merged.to_excel(output_path, index=False)

print(f'Результат сохранен в {output_path}')
