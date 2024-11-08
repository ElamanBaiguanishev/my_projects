import os
import pandas as pd

from bs4 import BeautifulSoup, NavigableString

html_files = [f for f in os.listdir("datas") if f.endswith('.html')]

data = {'User': [], 'Email': [], 'Group': []}

for file in html_files:
    with open(f"datas/{file}", encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        main_div = soup.find('div', {'class': 'bx-users'})
        user_divs = main_div.find_all("div", {'class': "bx-user-text"})
        for div in user_divs:
            user = div.find('div', {'class': 'bx-user-name'}).text.strip()
            properties = div.find('div', {'class': 'bx-user-properties'})
            email = properties.next.next.text
            try:
                group = properties.next.next.next.next.next.next.split("\n")[2].strip()
            except:
                print("\tТУТ ОШИБКА")
                print(properties.next.next.next.next.next.next.split("\n"))

            # Добавляем данные в словарь
            data['User'].append(user)
            data['Email'].append(email)
            data['Group'].append(group)

# Создаем DataFrame из словаря
df = pd.DataFrame(data)

# Записываем DataFrame в Excel-файл
df.to_excel('output.xlsx', index=False)
