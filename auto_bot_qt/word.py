import docx

# Открываем документ
doc = docx.Document('D:\Ответы\История транспорта2.docx')

found_question = False

questions = []

paragraphs = doc.paragraphs

for i in range(len(paragraphs)):
    if "Выберите один ответ:" in paragraphs[i].text:
        questions.append(paragraphs[i-1].text)
    if "+" in paragraphs[i].text:
        try:
            questions.append(paragraphs[i].text.split("\xa0")[1].replace("+", ""))
        except Exception as e:
            questions.append(paragraphs[i].text.replace("+", ""))

dictionary: dict = {questions[i]: questions[i + 1] for i in range(0, len(questions), 2)}

print(dictionary)

keys = list(dictionary.keys())
values = list(dictionary.values())

for i in range(len(keys)):
    print(keys[i], ":", values[i])