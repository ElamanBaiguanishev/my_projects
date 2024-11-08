import pywhisper as pw
from datetime import datetime
from os import listdir
from os.path import isfile, join


fileNames = [f for f in listdir("input") if isfile(join("input", f))]

modelName = "large"

# Выбор модели (вместо tiny можно написать base, small, medium и large)
model: pw.Whisper = pw.load_model("modelName")


# Цикл, обрабатывающий все файлы из списка
for i in range(len(fileNames)):
    print("Start Time:", datetime.now().strftime("%H:%M:%S"))
    fileName = fileNames[i]
    result = model.transcribe(str("input/" + fileName))
    file = open("output/" + str(fileName)[:-4] + ".txt", "w", encoding="utf-8")
    file.write(str(result["text"]))
    print(fileName + " completed!")
    print("End Time:", datetime.now().strftime("%H:%M:%S") + "\n")
