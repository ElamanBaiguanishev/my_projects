import random
import shutil
from os import listdir
from os import path
import ctypes




# for p in psutil.process_iter(['name']):
#     print(p.name())

ctypes.windll.user32.SystemParametersInfoW(20, 0, r'C:\Users\admin\PycharmProjects\zad3\desktop.jpg', 0)

files_desktop = listdir(f'D:\\look.com.ua_2016.02-111-1920x1080\\')
file_desktop = random.choice(files_desktop)

ctypes.windll.user32.SystemParametersInfoW(20, 0, 'D:\\look.com.ua_2016.02-111-1920x1080\\' + file_desktop, 0)

source_path = "C:\\Users\\admin\\Desktop\\"
destination_path = "C:\\Users\\admin\\Desktop\\files\\"
#
fileNames = listdir(source_path)
#
# os.startfile(source_path + random.choice(fileNames))
#
# print(fileNames)
#
for i in range(len(fileNames)):
    fileName = source_path + fileNames[i]
    if path.exists(fileName):
        new_location = shutil.move(fileName, destination_path)
        print("% s перемещен в указанное место,% s" % (fileName, new_location))
    else:
        print("Файл не существует.")

count = random.randint(10, 20)
fileNames2 = listdir(destination_path)

for j in range(count):
    fileName = random.choice(fileNames2)
    fileNames2.remove(fileName)
    fileName = destination_path + fileName
    print(fileName)
    if path.exists(fileName):
        new_location = shutil.move(fileName, source_path)
        print("% s перемещен в указанное место,% s" % (fileName, new_location))
    else:
        print("Файл не существует.")
# import os
#
# array = [
#     'Проекты',
#     'Личный',
#     'Работа',
#     'Школа',
#     'Финансовый',
#     'Чек',
#     'Архивы',
#     'Температура',
#     'Игры',
#     'Программное обеспечение',
#     'Изображения',
#     'Скриншоты',
#     'Шаблоны',
#     'Презентации',
#     'Электронные таблицы',
#     'Код',
#     'Записи',
#     'Электронные книги',
#     'Почта',
#     'Контакты',
#     'Общий',
#     'Веб-страницы',
#     'Архив загрузок',
#     'Разнообразный',
#     'Семья',
#     'Путешествовать',
#     'Расходы',
#     'Здоровье',
#     'Программы',
#     'Книги',
#     'Поступления',
#     'Налоги',
#     'Фото',
#     'Видео',
#     'Аудио',
#     'Личные финансы',
#     'Пишу',
#     'Исследование',
#     'Рабочие проекты',
#     'Графика',
#     'Анимация',
#     'Скрипты',
#     'Руководства',
#     'Счета-фактуры',
#     'Предложения',
#     'Контракты',
#     'Информация о клиенте',
#     'Информация о сотруднике',
#     'Резервные копии',
#     'Заставки',
#     'Шрифты',
#     'Значки',
#     'Темы',
#     'Плагины',
#     'Базы данных',
#     'Отчеты',
#     'Аналитика'
# ]
#
# for i in array:
#     name = 'C:\\Users\\admin\\Desktop\\files\\{}'.format(i)
#     if not os.path.exists(name):
#         os.mkdir(name)
#
# print("OK")