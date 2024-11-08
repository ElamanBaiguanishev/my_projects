from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import chardet
from aiogram.types import InputFile
import asyncio

from db import add_data, replace_data, clean_data, get_data, init_db
from tools import check_validate_requests

bot = Bot(token='6074471528:AAEz-tBGwiBoRrI7sd01lWMeVKi27Q5IkWo')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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
    data_ = get_data(message.from_id)
    limit = len(data_)
    if limit == 0:
        await message.answer('База данных пуста')
    else:
        kb = [
            [types.KeyboardButton(text="/stop")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await state.set_state(State.STARTED)
        await message.answer('Начало обработки', reply_markup=keyboard)
        count = 0
        while True:
            current_state = await state.get_state()
            if current_state != State.STARTED:
                break
            url_ = data_[count]
            if not check_validate_requests(url_):
                await message.answer(f"{url_} не валиден")
            asyncio.sleep(5)
            count = count + 1
            if count == limit:
                await message.answer("Лимит")
                count = 0


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

        current_state = await state.get_state()

        if current_state == "base":
            await message.answer("Перезаписываю..")
            count = replace_data(data_, id_)
            await message.answer(f"Было добавлено {count} записей")
            await state.finish()
            await db_start(message, state)
        elif current_state == "add":
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

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
