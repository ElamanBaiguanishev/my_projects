import json

import requests
from bs4 import BeautifulSoup
from group.print import total_keys_count

# URL for login
login_url = 'https://dot.omgups.ru/login/index.php'

ids = total_keys_count

login_payload = {
    'anchor': '',
    'logintoken': '',
    'username': "upyr_73se_233014",
    'password': "Upy#2988"
}

group_filename = "group/СЭ.json"

with requests.Session() as session:
    start = session.get(login_url)
    soup = BeautifulSoup(start.text, 'html.parser')
    logintoken_element = soup.find('input', {'name': 'logintoken'})
    login_payload["logintoken"] = logintoken_element.get('value')
    login_response = session.post(login_url, data=login_payload)

    if login_response.ok:
        print("Successful login!")

        user_id_min = 32635
        user_id_max = 33261
        # https://dot.omgups.ru/user/profile.php?id=33232

        buffer = {}
        count = 1
        while user_id_min <= user_id_max:
            user_id_min += 1
            if user_id_min not in ids:
                profile_response = session.get(f"https://dot.omgups.ru/user/profile.php?id={user_id_min}")
                profile_soup = BeautifulSoup(profile_response.text, 'html.parser')

                fio_div = profile_soup.find('div', {'class': 'page-header-headings'})

                group_element = profile_soup.select_one('dt:-soup-contains("Учебная группа") + dd')

                if group_element and fio_div:
                    fio = fio_div.text.strip()
                    group = group_element.text.strip()

                    buf = {
                        "group": group,
                        "ФИО": fio
                    }

                    print(f"{count} Добавил https://dot.omgups.ru/user/profile.php?id={user_id_min}")

                    buffer[str(user_id_min)] = buf
                else:
                    print(f"{count} Не найден https://dot.omgups.ru/user/profile.php?id={user_id_min}")
            count += 1

        with open(group_filename, encoding='utf-8') as group_file:
            existing_data = json.load(group_file)

        # Добавляем новые данные
        existing_data.update(buffer)

        with open(group_filename, 'w', encoding='utf-8') as group_file:
            json.dump(existing_data, group_file, ensure_ascii=False)

    else:
        print("Login error:", login_response.status_code)
