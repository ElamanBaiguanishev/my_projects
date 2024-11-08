from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import chardet
from aiogram.types import InputFile

from new_db import add_data, replace_data, clean_data, get_data, init_db
from tools import check_validate


# Определяем состояния
class State:
    STARTED = 'started'
    STARTED_DB = "start_db"
    BASE = "base"
    ADD = "add"
    CLEAN = "clean"


async def start_command(message: types.Message):
    photo = InputFile('example.png')
    id_ = message.bot.id
    init_db(id_)
    kb = [
        [types.KeyboardButton(text="/db")],
        [types.KeyboardButton(text="/processing")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    try:
        count = len(list(get_data(id_).values())[0])
    except Exception as e:
        print(e)
        count = 0
    await message.answer(
        f'Приветствую! Для того, чтобы начать работу, обновите базу данных.'
        f'\nТекущее количество записей {count}. Пример файла для загрузки:'
    )
    await message.answer_photo(photo,
                               reply_markup=keyboard)


async def start_processing(message: types.Message, state: FSMContext):
    data_ = list(get_data(message.bot.id).values())[0]
    if len(data_) == 0:
        await message.answer('База данных пуста')
    else:
        limit = len(data_)
        kb = [
            [types.KeyboardButton(text="/stop")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await state.set_state(State.STARTED)
        await message.answer('Начало обработки', reply_markup=keyboard)

        count = 0
        while True:
            # Проверяем текущее состояние
            current_state = await state.get_state()
            if current_state != State.STARTED:
                break  # Если состояние изменилось, прекращаем отправку сообщений
            url_ = data_[count]
            if not check_validate(url_):
                # Отправляем сообщение
                await message.answer(f"{url_} не валиден")
            count = count + 1
            if count == limit:
                await message.answer("Лимит")
                count = 0


async def stop_command(message: types.Message, state: FSMContext):
    await state.finish()
    kb = [
        [types.KeyboardButton(text="/db")],
        [types.KeyboardButton(text="/processing")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Бот прекратил отправку сообщений', reply_markup=keyboard)


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


async def db_document_message(message: types.Message, state: FSMContext):
    await state.update_data(document=message.document)
    kb = [
        [types.KeyboardButton(text="Да")],
        [types.KeyboardButton(text="Нет")],
        [types.KeyboardButton(text="Отмена")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Подтвердите загрузку файла', reply_markup=keyboard)


async def clean_base_message(message: types.Message, state: FSMContext):
    if message.text == "Да":
        await message.answer("Очищаю..")
        count = clean_data(message.bot.id)
        await message.answer(f"Было удалено {count} записей")
        await state.finish()
        await db_start(message, state)
    elif message.text == "Нет":
        await state.finish()
        await message.answer('Выполняю...')
        await db_start(message, state)
    else:
        await message.answer("Неверная команда")


async def db_base_message(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer('Выполняю...')
        await db_start(message, state)
    elif message.text == "Да":
        data = await state.get_data()
        dp = Dispatcher.get_current()
        bot = dp.bot
        document = data.get("document")
        file_info = await bot.get_file(document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Определение кодировки файла
        raw_data = downloaded_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        id_ = message.bot.id

        # Декодирование содержимого файла
        content = raw_data.decode(encoding)
        data_ = {message.from_id: content.splitlines()}

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
