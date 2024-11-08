from typing import Union

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from vkbottle.bot import Bot, Message, rules
from vkbottle.dispatch.rules import ABCRule
import random
from datetime import datetime, timedelta
import time

bot = Bot(token="81bea9a533ee468fd9ec03365deaf39c53370802d7fc4cac960d8f75bef4fbc5dbdc65d82a0b49daed084")


class MyRule(ABCRule[Message]):
    def __init__(self, lt: int = 1):
        self.lt = lt

    async def check(self, event: Message) -> bool:
        return len(event.text) > self.lt


bot.labeler.custom_rules["my_rule"] = MyRule


@bot.on.chat_message(text="HI")
async def reg_handler(message: Message):
    await message.answer(message=f"HI")


@bot.on.chat_message(my_rule=2)
async def reg_handler(message: Message):
    await message.answer(message=f"HI")


bot.run_forever()
