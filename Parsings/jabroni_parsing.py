import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import os

keywords = ["Squad Leaders", "Abilities", "Weapons", "Weapon Upgrades", "Researchable Upgrades", "Unit Upgrades",
            "Buildable Units", "Add-ons", "Researches"]


def sperma(_url, race_path):
    response = requests.get(_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    image_element = soup.find_all(class_="infobox")[0]

    sperma_ = image_element.find_all('td')

    name: str = sperma_[0].text.strip()

    path_ = race_path + f"{name}/"

    if not os.path.exists(path_):
        os.makedirs(path_)

    img_tag = sperma_[6].find('img')

    img_url = urljoin(_url, img_tag['src'])

    img_response = requests.get(img_url)

    filename = img_url.split('/')[-1]
    with open(f"{path_}/{filename}", 'wb') as f:
        f.write(img_response.content)

    headline_elements = soup.find_all(class_="mw-headline")
    headline_elements.remove(headline_elements[0])
    headline_elements.remove(headline_elements[-1])

    start_printing = False

    for headline in headline_elements:
        table_element = headline.find_next('table').find('img')
        if headline.text in keywords:
            start_printing = True

            path = path_ + headline.text

            if not os.path.exists(path):
                os.makedirs(path)
            continue
        if start_printing:
            img_url = urljoin(_url, table_element['src'])

            img_response = requests.get(img_url)

            filename = img_url.split('/')[-1]

            with open(f"{path}/{filename}", 'wb') as f:
                f.write(img_response.content)


with open("keker.json") as json_file:
    # Записать новые данные в файл JSON
    data: dict[str, dict[str, list[str]]] = json.load(json_file)

base_path = 'images/'

for key, value in data.items():
    path = base_path + key + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    for key_, value_ in value.items():
        path_1 = path + key_ + "/"
        if not os.path.exists(path_1):
            os.makedirs(path_1)
        for url in value_:
            sperma(_url="https://warhammer-guide.ru/wiki/" + url, race_path=path_1)
