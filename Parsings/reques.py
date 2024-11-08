import json
import re
from data import data

import requests
from bs4 import BeautifulSoup

# URL for login
login_url = 'https://dot.omgups.ru/login/index.php'


for login, password in data.items():
    login_payload = {
        'anchor': '',
        'logintoken': '',
        'username': login,
        'password': password
    }
    with requests.Session() as session:
        start = session.get(login_url)
        soup = BeautifulSoup(start.text, 'html.parser')
        logintoken_element = soup.find('input', {'name': 'logintoken'})
        login_payload["logintoken"] = logintoken_element.get('value')
        login_response = session.post(login_url, data=login_payload)

        if login_response.ok:
            print("Successful login!")

            user_id_soup = BeautifulSoup(login_response.text, 'html.parser')

            div_element = user_id_soup.find('div', {'class': 'popover-region',
                                                    'id': 'nav-notification-popover-container',
                                                    'data-region': 'popover-region'})

            user_id = int(div_element.get('data-userid'))
            print(user_id)
            # https://dot.omgups.ru/user/profile.php?id=33232

            buffer = {}

            while True:
                user_id -= 1
                if user_id <= 0:
                    break
                profile_response = session.get(f"https://dot.omgups.ru/user/profile.php?id={user_id}")
                profile_soup = BeautifulSoup(profile_response.text, 'html.parser')

                fio_div = profile_soup.find('div', {'class': 'page-header-headings'})

                group_element = profile_soup.select_one('dt:-soup-contains("Учебная группа") + dd')

                if group_element and fio_div:
                    fio = fio_div.text.strip()
                    group = group_element.text.strip()

                    data = {"фио": fio, "группа": group}

                    buf = {
                        "Группа": group,
                        "user_id": user_id
                    }

                    buffer[fio] = buf
                else:
                    break

            user_id = int(div_element.get('data-userid'))

            while True:
                user_id += 1
                if user_id <= 0:
                    break
                profile_response = session.get(f"https://dot.omgups.ru/user/profile.php?id={user_id}")
                profile_soup = BeautifulSoup(profile_response.text, 'html.parser')

                fio_div = profile_soup.find('div', {'class': 'page-header-headings'})

                group_element = profile_soup.select_one('dt:-soup-contains("Учебная группа") + dd')

                if group_element and fio_div:
                    fio = fio_div.text.strip()
                    group = group_element.text.strip()

                    data = {"фио": fio, "группа": group}

                    buf = {
                        "Группа": group,
                        "user_id": user_id
                    }

                    buffer[fio] = buf
                else:
                    break

            print(buffer)
            json_data = json.dumps(buffer, ensure_ascii=False)

            with open(f'data/{login}.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json_data)

        else:
            print("Login error:", login_response.status_code)
