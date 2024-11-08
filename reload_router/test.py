import pandas as pd
import re

# Загрузка данных из result.xlsx
result_df = pd.read_excel('result_dot.xlsx')


# Функция для извлечения нужной информации из текста
def extract_group(text):
    if pd.notna(text):  # Проверка на пустую ячейку
        group = re.sub(r'[^A-Za-zА-Яа-я]', '', text)
        return group
    else:
        return None


# Применение функции к столбцу 'Текст'
result_df['Group'] = result_df['Group'].apply(extract_group)

# Запись результата в файл final_result.xlsx
result_df.to_excel('final_result2.xlsx', index=False)
