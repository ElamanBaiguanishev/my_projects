import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import ClientSession

bot = Bot(token="6733029434:AAHIaq965YS110m9m50cP0DcnvkD_pwa8CE", parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    arr = []
    for i in range(1000):
        async with ClientSession() as session:
            response = await session.get('https://ipinfo.io/json')
            data = await response.json()
            arr.append(data['ip'])
    await message.answer(str(set(arr)))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
