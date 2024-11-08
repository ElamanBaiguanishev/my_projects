import requests
# from difflib import Differ
#
# url1 = "https://t.me/user42"
# url2 = "https://t.me/user13"
#
# response1 = requests.get(url1).text
# response2 = requests.get(url2).text
#
# # Разделители строк для разницы
# line_separator = '\n'
#
# # Разделяем строки HTML-кода
# html_lines1 = response1.splitlines()
# html_lines2 = response2.splitlines()
#
# # Создаем объект Differ
# differ = Differ()
#
# # Сравниваем строки HTML-кода
# diff = differ.compare(html_lines1, html_lines2)
#
# # Фильтруем различия
# diff = [line for line in diff if line.startswith('-') or line.startswith('+')]

for i in range(100):
    print(f"https://t.me/user{i+100}")

# Выводим различия
# print("Отличия в HTML-коде:")
# print(line_separator.join(diff))
