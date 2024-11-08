import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import chardet
from aiogram.types import InputFile
import json
import sqlite3

from tools import check_validate

TOKENS = [
    '6074471528:AAEz-tBGwiBoRrI7sd01lWMeVKi27Q5IkWo', '6324885383:AAG6t1M2ii1qLwBjEaxY7QMwW7MMt_sHIKw',
    '6318444504:AAEaOhDTL9smyxw_u5FAbE3ExhmjzMZfqAM', '6210784198:AAHbTq68RXKAq0Ly6v94y5pJCN-Fd_Sq_1c',
    '6310541424:AAF4DpF73-RWCv5CdNICvAtGwC7A2qxFVWs', '6292095596:AAGm00y_clqttUZ9FHqHnkduHP9wa6N9kQQ'
]


async def bot_polling(token, index):
    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    conn = sqlite3.connect(f'data{index}.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            text TEXT
        )
    ''')

    def init_db(id_: int):
        try:
            cursor.execute('INSERT INTO data (id, text)  VALUES (?, ?)', (id_, "[]"))

            conn.commit()
        except Exception as e:
            print("init_db", e)

    def get_data(id_: int) -> list:
        try:
            cursor.execute('SELECT * FROM data WHERE id = ?', (id_,))
            record = cursor.fetchone()

            data_list = json.loads(record[1])

            conn.commit()
            return data_list
        except Exception as e:
            print("get_data", e)
            return []

    def replace_data(data_, id_: int) -> int:
        try:
            sql_query = f"UPDATE data SET text = ? WHERE id = ?"

            cursor.execute(sql_query, (json.dumps(data_), id_))

            # Сохраняем изменения и закрываем соединение
            conn.commit()

            return len(data_)
        except Exception as e:
            print("replace_data", e)
            return 0

    def add_data(data_, id_: int) -> int:
        try:
            old_data = get_data(id_)

            new_data = set(old_data + data_)

            replace_data(list(new_data), id_)

            conn.commit()

            return len(new_data) - len(old_data)
        except Exception as e:
            print("add_data", e)
            return 0

    def clean_data(id_: int) -> int:
        try:
            old_data = get_data(id_)

            replace_data([], id_)

            conn.commit()

            return len(old_data)
        except Exception as e:
            print("clean_data", e)
            return 0

    class State:
        STARTED = 'started'
        STARTED_DB = "start_db"
        BASE = "base"
        ADD = "add"
        CLEAN = "clean"

    @dp.message_handler(Command('start'), state=None)
    async def start_command(message: types.Message):
        photo = InputFile('example.png')
        id_ = message.from_id
        bot_info = await bot.get_me()
        bot_id = bot_info.id
        print(bot_id)
        init_db(id_)
        kb = [
            [types.KeyboardButton(text="/db")],
            [types.KeyboardButton(text="/processing")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            f'Приветствую! Для того, чтобы начать работу, обновите базу данных.'
            f'\nТекущее количество записей {len(get_data(id_))}. Пример файла для загрузки:'
        )
        await message.answer_photo(photo,
                                   reply_markup=keyboard)

    @dp.message_handler(Command('processing'), state=None)
    async def start_processing(message: types.Message, state: FSMContext):
        global current_state
        data_ = get_data(message.from_id)
        if len(data_) == 0:
            await message.answer('База данных пуста')
        else:
            kb = [
                [types.KeyboardButton(text="/stop")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await state.set_state(State.STARTED)
            await message.answer('Начало обработки', reply_markup=keyboard)

            while True:
                for i in data_:
                    current_state = await state.get_state()
                    if current_state != State.STARTED:
                        break
                    task = check_validate(i)
                    if not task:
                        await message.answer(i)
                if current_state != State.STARTED:
                    break

    @dp.message_handler(Command('stop'), state=State.STARTED)
    async def stop_command(message: types.Message, state: FSMContext):
        await state.finish()
        kb = [
            [types.KeyboardButton(text="/db")],
            [types.KeyboardButton(text="/processing")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Бот прекратил отправку сообщений', reply_markup=keyboard)

    @dp.message_handler(Command("db"), state=None)
    async def db_start(message: types.Message, state: FSMContext):
        kb = [
            [types.KeyboardButton(text="Записать данные")],
            [types.KeyboardButton(text="Перезаписать данные")],
            [types.KeyboardButton(text="Очистить данные")],
            [types.KeyboardButton(text="Выйти из БД")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Запущена работа с базой...", reply_markup=keyboard)
        await state.set_state(State.STARTED_DB)

    @dp.message_handler(state=State.STARTED_DB)
    async def db_handle_message(message: types.Message, state: FSMContext):
        if message.text == "Перезаписать данные":
            await state.set_state(State.BASE)
            kb = [
                [types.KeyboardButton(text="Отмена")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer('Прикрепите документ с данными. Все данные в базе заменятся на новые',
                                 reply_markup=keyboard)
        elif message.text == "Записать данные":
            await state.set_state(State.ADD)
            kb = [
                [types.KeyboardButton(text="Отмена")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer('Прикрепите документ с данными. К старым данным будут добавлены новые',
                                 reply_markup=keyboard)
        elif message.text == "Очистить данные":
            await state.set_state(State.CLEAN)
            kb = [
                [types.KeyboardButton(text="Да")],
                [types.KeyboardButton(text="Нет")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer('База данных будет очищена. Очистить базу?', reply_markup=keyboard)
        elif message.text == "Выйти из БД":
            await state.finish()
            kb = [
                [types.KeyboardButton(text="/db")],
                [types.KeyboardButton(text="/processing")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выход....", reply_markup=keyboard)
        else:
            await message.answer('Нажмите на команду либо введите ее вручную')

    @dp.message_handler(state=[State.BASE, State.ADD], content_types=types.ContentType.DOCUMENT)
    async def db_document_message(message: types.Message, state: FSMContext):
        await state.update_data(document=message.document)
        kb = [
            [types.KeyboardButton(text="Да")],
            [types.KeyboardButton(text="Нет")],
            [types.KeyboardButton(text="Отмена")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Подтвердите загрузку файла', reply_markup=keyboard)

    @dp.message_handler(state=State.CLEAN)
    async def clean_base_message(message: types.Message, state: FSMContext):
        if message.text == "Да":
            await message.answer("Очищаю..")
            count = clean_data(message.from_id)
            await message.answer(f"Было удалено {count} записей")
            await state.finish()
            await db_start(message, state)
        elif message.text == "Нет":
            await state.finish()
            await message.answer('Выполняю...')
            await db_start(message, state)
        else:
            await message.answer("Неверная команда")

    @dp.message_handler(state=[State.BASE, State.ADD])
    async def db_base_message(message: types.Message, state: FSMContext):
        if message.text == "Отмена":
            await state.finish()
            await message.answer('Выполняю...')
            await db_start(message, state)
        elif message.text == "Да":
            data = await state.get_data()
            document = data.get("document")
            file_info = await bot.get_file(document.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)

            # Определение кодировки файла
            raw_data = downloaded_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            id_ = message.from_id
            print(encoding)

            # Декодирование содержимого файла
            content = raw_data.decode(encoding)
            data_ = content.splitlines()

            current_state_ = await state.get_state()

            if current_state_ == "base":
                await message.answer("Перезаписываю..")
                count = replace_data(data_, id_)
                await message.answer(f"Было добавлено {count} записей")
                await state.finish()
                await db_start(message, state)
            elif current_state_ == "add":
                await message.answer("Записываю..")
                count = add_data(data_, id_)
                await message.answer(f"Было добавлено {count} записей")
                await state.finish()
                await db_start(message, state)
        elif message.text == "Нет":
            await state.reset_data()
            kb = [
                [types.KeyboardButton(text="Отмена")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer(f"Прикрепите новый документ", reply_markup=keyboard)
        else:
            await message.answer("Прикрепите документ")

    await dp.start_polling()


async def main():
    tasks = [bot_polling(token, count) for count, token in enumerate(TOKENS)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
