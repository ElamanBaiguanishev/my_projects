import json

from data import data

count = 0
b = []

for login in data:
    with open(f"data/{login}.json", encoding='utf-8') as json_file:
        d: dict = json.load(json_file)
        # print(len(d.keys()))
        count += len(d.keys())

        keys_list = list(d.keys())
        a = d[keys_list[0]]["user_id"]
        b.append(int(a))
        # print(a)
        # for fio, info in d.items():
        #     print(info)

print(min(b))
print(max(b))
print(max(b) - min(b))
print(count)
