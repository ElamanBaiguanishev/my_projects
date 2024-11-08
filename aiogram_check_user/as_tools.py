import requests
from bs4 import BeautifulSoup

# Читаем прокси из файла
with open('actual_proxy.txt') as file:
    proxies = file.read().splitlines()

print(proxies)

# URL, который вы хотите запросить
# url = 'https://t.me/user0'

# Проходим по каждому прокси
for proxy in proxies:
    # Разбиваем строку прокси на компоненты
    proxy_parts = proxy.split(':')
    print(proxy_parts)
    proxy_host = proxy_parts[0]
    proxy_port = int(proxy_parts[1])
    proxy_username = proxy_parts[2]
    proxy_password = proxy_parts[3]

    with open('kek.txt', "a") as file:
        file.write(f'{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}\n')
    # Создаем словарь с параметрами прокси
    # proxy_dict = {
    #     'http': f'{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
    #     'https': f'{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
    # }
    #
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    # }
    #
    # try:
    #     response = requests.get(url='https://t.me/user0', headers=headers, proxies=proxy_dict)
    #     print(response.text)
    # except requests.RequestException as e:
    #     print(f"Error using proxy {proxy_dict}: {str(e)}")
