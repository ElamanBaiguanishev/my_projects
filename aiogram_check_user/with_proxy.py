import requests

with open('actual_proxy.txt') as f:
    lines = f.read().splitlines()


def check_proxy(proxy):
    url = "https://t.me/user717"  # Можете заменить на любой другой сайт для проверки

    proxies = {
        "http": proxy,
        "https": proxy,
    }

    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()

        # Печать протоколов, если запрос успешен
        print(f"Прокси {proxy} работает. Используемые протоколы: {response.request.scheme}")
    except requests.exceptions.RequestException as e:
        # Если возникла ошибка, то прокси не работает
        print(f"Прокси {proxy} не работает. Ошибка: {e}")


# Проверка каждого прокси из списка
for proxy in lines:
    check_proxy(proxy)
