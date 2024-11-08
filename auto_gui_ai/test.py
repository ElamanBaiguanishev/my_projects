with open('adapters.txt', encoding='utf-8') as file:
    file_content = set(file.read().splitlines())

for i in file_content:
    print(i)
