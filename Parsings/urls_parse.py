import json

import requests
from bs4 import BeautifulSoup

url = "https://warhammer-guide.ru/wiki/Dawn_of_War_Players_Guide.html"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Найдем все элементы с классом "toccolours"
infobox_elements = soup.find_all(class_="toccolours")[0].find_all("td")

races = ["Space Marine",
         "Chaos",
         "Eldar",
         "Orks",
         "Imperial Guard",
         "Tau",
         "Necrons",
         "Dark Eldar",
         "Sisters of Battle"]

str_ = {}

for i, race in enumerate(races):
    str_[race] = {
        "Infantry": [
            a_tag.get("href") for a_tag in infobox_elements[i].find_all("a")
        ],
        "Vehicles": [
            a_tag.get("href") for a_tag in infobox_elements[i + 9].find_all("a")
        ],
        "Buildings": [
            a_tag.get("href") for a_tag in infobox_elements[i + 18].find_all("a")
        ]
    }

with open("keker.json", "w") as json_file:
    # Записать новые данные в файл JSON
    json.dump(str_, json_file)
