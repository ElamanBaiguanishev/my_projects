import random

import requests


def get_proxy():
    """Gets a proxy from the proxy scrape service."""
    response = requests.get('https://www.proxyscrape.com/')
    print(response.text)
    data = response.json()
    proxy = random.choice(data['results'])['ip'] + ':' + data['results'][0]['port']
    return proxy


print(get_proxy())
