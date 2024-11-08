import docx

# Открываем документ
doc = docx.Document('D:\Ответы\История транспорта3.docx')

found_question = False

questions = []

paragraphs = doc.paragraphs

for i in range(len(paragraphs)):
    if "Правильный ответ" in paragraphs[i].text:
        questions.append(paragraphs[i - 1].text)
        questions.append(paragraphs[i].text.replace("Правильный ответ: ", ""))

print(questions)
dictionary: dict = {questions[i]: questions[i + 1] for i in range(0, len(questions), 2)}

print(dictionary)

keys = list(dictionary.keys())
values = list(dictionary.values())

for i in range(len(keys)):
    print(keys[i], ":", values[i])
