import random
import pandas as pd


def data():
    with open('adapters.txt', encoding='utf-8') as file:
        file_content = file.read().splitlines()
    result = []
    for _, row in pd.read_excel("db\\students.xlsx", header=None,
                                skiprows=1).iterrows():
        result.append({
            "f": row[2].strip(),
            "i": row[3].strip(),
            "o": row[4].strip(),
            "group": row[5].strip(),
            "adapter": random.choice(file_content),
            "login": row[0].strip(),
            "password": row[1].strip(),
            "url": row[6].strip()
        })

    return result
