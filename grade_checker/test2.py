import re

group_en_to_ru = {
    "at": "АТ",
    "gv": "ГВ",
    "im": "ИМ",
    "ip": "ИП",
    "lt": "ЛТ",
    "le": "ЛЭ",
    "ng": "НГ",
    "od": "ОД",
    "pv": "ПВ",
    "pt": "ПТ",
    "rs": "РС",
    "sp": "СП",
    "se": "СЭ",
    "tb": "ТБ",
    "td": "ТД",
    "tl": "ТЛ",
    "tm": "ТМ",
    "tr": "ТР",
    "eb": "ЭБ",
    "bd": "БД"
}


def transform_string(input_str):
    parts = input_str.split('_')
    len_parts = len(parts)
    if len_parts > 1:
        part1 = re.sub(r'[^\w\s]+|[\d]+', r'', parts[1]).strip()
        part2 = parts[2]
        if len_parts > 3:
            return f"{group_en_to_ru[part1]}-{part2}-{parts[3]}"
        else:
            if len(parts[2]) < 6 or len(parts[2]) > 6:
                return f"{group_en_to_ru[part1]}-{part2}"
            else:
                return f"{group_en_to_ru[part1]}-{part2[:2]}-{part2[2:]}"
    else:
        print(input_str)



# Example usage
input_str1 = "karablin_73sp­_232079"
input_str2 = "skakovdb-at-223376"
input_str3 = "zhitov_70tb_7224"

print(transform_string(input_str1))
print(transform_string(input_str2))
print(transform_string(input_str3))
