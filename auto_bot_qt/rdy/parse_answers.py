import pandas as pd


def answers(name: str) -> dict[str, list[str]]:
    path = f"answers/{name}.xlsx"
    answers_ = {}
    df = pd.read_excel(path, header=None, skiprows=1)

    for _, row in df.iterrows():
        key = row[0].replace("\xa0", " ")  # Удаление неразрывных пробелов
        values = [item.replace("\xa0", " ") for item in str(row[1]).split(";")]
        answers_[key] = values

    return answers_
