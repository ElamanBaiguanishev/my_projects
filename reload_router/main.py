import time

import requests

# URL для входа
login_url = 'https://portal.omgups.ru/auth/?login=yes&backurl=%2Fextranet%2F'

# URL для GET-запроса
get_url = 'https://portal.omgups.ru/extranet/contacts/'
# логин NosikovAD пароль 623722Ok.21
# Данные для входа
login_payload = {
    'AUTH_FORM': 'Y',
    'TYPE': 'AUTH',
    'backurl': '/auth/?backurl=%2Fextranet%2F',
    'USER_LOGIN': 'NosikovAD',
    'USER_PASSWORD': '623722Ok.21'
}

# Параметры для GET-запроса
# get_params = {
#     'bxajaxid': '9684b36fc6960bb92b064139ff3e5e70',
#     'AJAX_CALL': 'Y',
#     'current_view': 'list',
#     'current_filter': 'simple',
#     'contacts_search_UF_EDU_STRUCTURE': '73',
#     'contacts_search_FIO': 'Калинин Константин',
#     'set_filter_contacts_search': 'Y',
#     'set_filter_contacts_search': 'Найти'
# }

# Создание сессии
with requests.Session() as session:
    # Отправка POST-запроса для входа
    login_response = session.post(login_url, data=login_payload)

    # Проверка успешности входа
    if login_response.ok:
        print("Успешный вход!")

        # Теперь отправим GET-запрос с параметрами
        for i in range(188):
            response = session.get(f"https://portal.omgups.ru/extranet/contacts/?PAGEN_1={i + 1}")
            if response.ok:
                print("Данные получены:", response.status_code)
                with open(f"datas/page{i + 1}.html", "w", encoding='utf-8') as file:
                    file.write(response.text)
            else:
                print("Ошибка при получении данных:", response.status_code)
            time.sleep(5)
    else:
        print("Ошибка входа:", login_response.status_code)

for i in range(188):
    print(i + 1)
