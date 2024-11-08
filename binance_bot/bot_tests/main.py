import asyncio

from bot_tests.bot1 import dp1
from bot_tests.bot2 import dp2


async def start_bots():
    await asyncio.gather(dp1.start_polling(), dp2.start_polling())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bots())
