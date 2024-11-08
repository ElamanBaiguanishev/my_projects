import datetime
import logging
import sys
import asyncio
import random
import time
import traceback

import aiohttp
import chardet
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiohttp import ClientSession

from config import *
from db import get_proxy, init_db, get_data, init_proxy, replace_data, replace_proxy

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


class Form(StatesGroup):
    PROXY = State()
    USERS = State()
    USERS_PROCESS = State()
    # ADD = State()
    # CLEAN = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    kb = [
        [types.KeyboardButton(text="Прокси")],
        [types.KeyboardButton(text="Ссылки юзеров")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=keyboard)


@dp.message(F.text == "Прокси")
async def proxy_start_handler(message: Message, state: FSMContext) -> None:
    init_proxy(message.from_user.id)
    await state.set_state(Form.PROXY)
    kb = [
        [types.KeyboardButton(text="get")],
        [types.KeyboardButton(text="exit")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Добавьте файл с прокси", reply_markup=keyboard)


@dp.message(F.text == "get", Form.PROXY)
async def get_proxy_handler(message: Message) -> None:
    proxys = get_proxy(message.from_user.id)
    proxy_list_str = "\n".join([f"{count}) {proxy_}" for count, proxy_ in enumerate(proxys, start=1)])
    max_message_length = 4096
    split_proxy_list = [proxy_list_str[i:i + max_message_length] for i in
                        range(0, len(proxy_list_str), max_message_length)]
    for part in split_proxy_list:
        await message.answer(part)


@dp.message(F.text == "exit", Form.USERS)
@dp.message(F.text == "exit", Form.PROXY)
async def proxy_exit_handler(message: Message, state: FSMContext) -> None:
    kb = [
        [types.KeyboardButton(text="Прокси")],
        [types.KeyboardButton(text="Ссылки юзеров")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"ok", reply_markup=keyboard)
    await state.clear()


@dp.message(F.document, Form.PROXY)
async def add_proxy_handler(message: Message) -> None:
    document = message.document
    file_info = await bot.get_file(document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    raw_data = downloaded_file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    content = raw_data.decode(encoding)
    data_ = content.splitlines()
    if replace_proxy(message.from_user.id, data_) != 0:
        await message.answer("Прокси успешно загружены")
    else:
        await message.answer("Ошибка")


@dp.message(F.text == "Ссылки юзеров")
async def users_handler(message: Message, state: FSMContext) -> None:
    init_db(message.from_user.id)
    await state.set_state(Form.USERS)
    kb = [
        [types.KeyboardButton(text="начать")],
        [types.KeyboardButton(text="exit")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Добавьте файл с юзерами", reply_markup=keyboard)


# @dp.message(F.text == "начать", Form.USERS)
# async def users_start_handler(message: Message, state: FSMContext) -> None:
#     proxies = get_proxy(message.from_user.id)
#     # proxies.append(None)
#     users = get_data(message.from_user.id)
#     await state.set_state(Form.USERS_PROCESS)
#     kb = [
#         [types.KeyboardButton(text="stop")]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
#     await message.answer("начинаю", reply_markup=keyboard)
#
#     # async def check_validate_requests_async(session, url, proxy_dict=None):
#     #     try:
#     #         async with session.get(url, proxy=proxy_dict) as response:
#     #             if response.status == 200:
#     #                 page_content = await response.text()
#     #                 if "tgme_page_icon" in page_content:
#     #                     await message.answer(f"Не валиден {url}")
#     #                     return False
#     #             return True
#     #     except:
#     #         await check_validate_requests_async(session, url, f'http://{random.choice(proxies)}')
#
#     loos = []
#
#     # async def check_validate_requests_async(session: ClientSession, url, proxy_dict=None, timeout=40):
#     #     try:
#     #         async with session.get(url, proxy=proxy_dict, timeout=timeout) as response:
#     #             if "robots" in await response.text():
#     #                 await message.answer(f"Не валиден {url}")
#     #     except:
#     #         loos.append(proxy_dict)
#     #         prox = list(set(proxies) - set(loos))
#     #         await check_validate_requests_async(session, url, f'http://{random.choice(prox)}', 20)
#
#     async def check_validate_requests_async(session: ClientSession, url, proxy_dict=None, timeout=40):
#         try:
#             async with session.get(url, proxy=proxy_dict, timeout=timeout) as response:
#                 if "robots" in await response.text():
#                     await message.answer(f"Не валиден {url}")
#         except:
#             loos.append(proxy_dict)
#             prox = list(set(proxies) - set(loos))
#             await check_validate_requests_async(session, url, f'http://{random.choice(prox)}', 20)
#
#     while await state.get_state() == Form.USERS_PROCESS:
#         loos = []
#         async with ClientSession() as session:
#             tasks = [check_validate_requests_async(session, url, f'http://{proxies[i % len(proxies)]}') for i, url in
#                      enumerate(users)]
#             await asyncio.gather(*tasks)
#     else:
#         kb = [
#             [types.KeyboardButton(text="начать")],
#             [types.KeyboardButton(text="exit")]
#         ]
#         keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
#         await message.answer("остановка", reply_markup=keyboard)


@dp.message(F.text == "начать", Form.USERS)
async def users_start_handler(message: Message, state: FSMContext) -> None:
    try:
        proxies = get_proxy(message.from_user.id)
        users = get_data(message.from_user.id)
        await state.set_state(Form.USERS_PROCESS)
        kb = [
            [types.KeyboardButton(text="stop")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("начинаю", reply_markup=keyboard)

        async def check_validate_requests_async(url, proxy_dict=None, timeout=40):
            try:
                async with ClientSession() as session:
                    response = await session.get(url, proxy=proxy_dict, timeout=timeout)
                    if "robots" in await response.text():
                        # await message.answer(f"Не валиден {url}")
                        urls.append(url)
            except:
                await check_validate_requests_async(url=url, timeout=20)

        total_seconds: list[float] = []
        while await state.get_state() == Form.USERS_PROCESS:
            urls = []
            time_start = datetime.datetime.now()
            tasks = [check_validate_requests_async(url, f'http://{proxies[i % len(proxies)]}') for i, url in
                     enumerate(users)]
            await asyncio.gather(*tasks)
            print(f"кол-во символов {len(str(urls))}")
            await message.answer(f"{urls}")
            await message.answer(f"Прошел")

            time_end = datetime.datetime.now()
            total_seconds.append((time_end - time_start).total_seconds())
        else:
            kb = [
                [types.KeyboardButton(text="начать")],
                [types.KeyboardButton(text="exit")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer(f"остановка {sum(total_seconds) / len(total_seconds)}", reply_markup=keyboard)
    except Exception as e:
        traceback.print_exc()
        print(f"ОШИБКААА {e}")


@dp.message(Form.USERS_PROCESS)
async def start_process_handler(message: Message, state: FSMContext) -> None:
    if message.text == "stop":
        await state.set_state(Form.USERS)
        await message.answer("Останавливаю процесс, ждите")
    else:
        await message.answer("Сейчас идет процесс обработки ссылок")


@dp.message(F.document, Form.USERS)
async def add_proxy_handler(message: Message) -> None:
    document = message.document
    file_info = await bot.get_file(document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    raw_data = downloaded_file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    content = raw_data.decode(encoding)
    data_ = content.splitlines()
    new_data = replace_data(data_, message.from_user.id)
    if new_data != 0:
        await message.answer(f"Прокси успешно загружены. Кол-во записей {new_data}")
    else:
        await message.answer("Ошибка")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
