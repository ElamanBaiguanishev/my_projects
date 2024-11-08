import json
import time

import pyautogui as pg

from coord import coord
from create_dox import create_dox

layout = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                           'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                  "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                  'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))


def pg_ai():
    with open('data_ct.json', encoding='utf-8') as file:
        file_content = file.read()

    # Преобразуем содержимое файла в словарь
    data_ct = json.loads(file_content)

    second_name = data_ct["f"]
    first_name = data_ct["i"]
    o = data_ct["o"]
    group = data_ct["group"]
    time.sleep(1)
    pg.hotkey("win", "r")
    time.sleep(1)

    pg.typewrite('ms-settings:otherusers')
    pg.press('enter')

    time.sleep(1)

    pg.click(coord(pg.screenshot(), "Добавить"))

    time.sleep(1)

    while True:
        if coord(pg.screenshot(), "Подождите") is None:
            print("Ожидание завершилось")
            break

    time.sleep(1)

    pg.click(coord(pg.screenshot(), "данных"))

    while True:
        if coord(pg.screenshot(), "Подождите") is None:
            print("Ожидание завершилось")
            break

    time.sleep(1)

    pg.click(coord(pg.screenshot(), "Добавить"))
    time.sleep(3)
    pg.hotkey("shift", "alt")
    pg.typewrite(second_name.translate(layout))
    time.sleep(3)
    pg.moveTo(x=920, y=110)
    pg.mouseDown()
    time.sleep(1)
    pg.dragTo(x=709, y=161, duration=1)
    pg.mouseUp()
    pg.screenshot("1.png")
    pg.hotkey("shift", "alt")
    pg.hotkey("alt", "f4")
    pg.hotkey("alt", "f4")
    time.sleep(1)

    pg.hotkey("win", "r")
    time.sleep(1)

    pg.typewrite('cmd')
    pg.press('enter')
    pg.hotkey("win", "up")
    time.sleep(300)
    pg.typewrite('dir.exe')
    pg.press('enter')
    time.sleep(1)
    pg.scroll(1300)
    time.sleep(1)
    pg.screenshot("2.png")
    pg.scroll(-300)
    time.sleep(1)
    pg.screenshot("3.png")
    pg.scroll(-950)
    time.sleep(1)
    pg.screenshot("4.png")

    create_dox(second_name, first_name, o, group)
