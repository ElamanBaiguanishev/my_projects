import json

import pandas as pd


def answers(name: str) -> dict[str, list[str]]:
    with open("resources/path.json") as json_file:
        data_json = json.load(json_file)
        path = data_json["answers"] + f"/{name}.xlsx"
    answers_ = {}
    df = pd.read_excel(path, header=None, skiprows=1)

    for _, row in df.iterrows():
        key = row[0].replace("\xa0", " ")  # Удаление неразрывных пробелов
        buff_array = []
        count = 1
        while True:
            try:
                if pd.isna(row[count]):
                    break
                else:
                    buff_array.append(row[count])
                count += 1
            except KeyError:
                break

        answers_[key] = buff_array

    return answers_
