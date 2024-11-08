import pandas as pd

# Загрузка данных из list.xlsx и output.xlsx
list_df = pd.read_excel('list.xlsx')
output_df = pd.read_excel('output.xlsx')

# Объединение данных по столбцу 'User' (ФИО)
result_df = pd.merge(list_df, output_df, how='left', left_on='ФИО', right_on='User')

# Удаление дублирующегося столбца 'User'
result_df = result_df.drop(columns=['User'])

# Разделение строк с несколькими ФИО
result_df['ФИО'] = result_df['ФИО'].str.split(', ')

# Применение explode для разделенных строк
result_df = result_df.explode('ФИО')

# Запись результата в файл result.xlsx
result_df.to_excel('result.xlsx', index=False)
