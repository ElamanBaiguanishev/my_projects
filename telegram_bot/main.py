import asyncio
import logging
import re
import sys
import psycopg2

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.markdown import hbold

from config import *
from db import quiz

form_router = Router()

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)


class Form(StatesGroup):
    STARTED = State()
    CHOICE_TEST = State()
    STARTED_TEST = State()
    END_TEST = State()
    ADD = State()
    CLEAN = State()


@form_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=ReplyKeyboardRemove())
    # with connection.cursor() as cursor:
    #     cursor.execute(f"INSERT INTO public.users (user_id) VALUES ({message.from_user.id})")
    #     connection.commit()
    #     print("Добавленно", message.from_user.id)
    await state.set_state(Form.STARTED)
    await state.set_data({"message_id": None, "current_question": 1})


@form_router.message(Command("item"), Form.STARTED)
async def choice_test(message: types.Message, state: FSMContext) -> None:
    entities = message.parse_entities(types.MessageEntity.TEXT_MENTION)

    if entities:
        # Если есть упоминания, извлекаем user_id из первого упоминания
        user_id = entities[0].user.id
        await message.answer(f"User ID: {user_id}")
    else:
        await message.answer("Вы не указали упоминание пользователя после команды /item.")


@form_router.message(Command("testing"), Form.STARTED)
async def start_test(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.STARTED_TEST)
    question = quiz[1]
    answers = [InlineKeyboardButton(text=i, callback_data=i) for i in question["answers"]]

    menu = InlineKeyboardMarkup(inline_keyboard=[answers])

    await message.answer("Начат тест!")
    message = await message.answer(text=question["question"], reply_markup=menu)
    await state.update_data(message_id=message.message_id)


@form_router.callback_query(lambda callback_query: callback_query.data, Form.STARTED_TEST)
async def process_callback(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    button_data = callback_query.data
    state_info = await state.get_data()
    message_id = state_info["message_id"]
    current_question = state_info["current_question"]

    quiz[current_question]["user_answer"] = button_data

    if current_question + 1 > len(quiz):
        await callback_query.answer("Это последний вопрос.")
        await state.set_state(Form.STARTED)
        await bot.edit_message_text(text=f"{[quiz[i + 1]['user_answer'] for i in range(len(quiz))]}",
                                    chat_id=callback_query.message.chat.id,
                                    message_id=message_id)
        await state.set_data({"message_id": None, "current_question": 1})
        return

    question = quiz[current_question + 1]
    answers = [InlineKeyboardButton(text=i, callback_data=i) for i in question["answers"]]

    menu = InlineKeyboardMarkup(inline_keyboard=[answers])

    await bot.edit_message_text(text=question["question"],
                                chat_id=callback_query.message.chat.id,
                                message_id=message_id,
                                reply_markup=menu)

    # Обновляем состояние
    await state.update_data(message_id=message_id, current_question=current_question + 1)


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
