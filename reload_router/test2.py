import pandas as pd

# Загрузка данных из final_result.xlsx и final_result2.xlsx
final_result_df = pd.read_excel('final_result.xlsx')
final_result2_df = pd.read_excel('final_result2.xlsx')

# Замена столбца 'Group' в final_result.xlsx, только где есть данные для замены
final_result_df['Group'] = final_result2_df['Group'].combine_first(final_result_df['Group'])

# Запись результата в файл final_result_updated.xlsx
final_result_df.to_excel('final_result_updated.xlsx', index=False)
