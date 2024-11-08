import logging
import sys
import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я – первокурсник", callback_data="freshman")]
    ])

    await message.answer(
        text=(
            f"Приветствую, {html.bold(message.from_user.full_name)}!"
        ),
        reply_markup=keyboard
    )


@dp.callback_query(lambda c: c.data == "freshman")
async def form_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бюджетное обучение", callback_data="form_budget")],
        [InlineKeyboardButton(text="Целевое обучение", callback_data="form_target")],
        [InlineKeyboardButton(text="Коммерческое обучение", callback_data="form_commerce")]
    ])

    await callback_query.message.answer(
        text=(
            f"Привет, первокурсник!\n"
            f"Твоя сессия с 10 февраля по 1 марта 2025 г.\n"
            f"На какую форму обучения ты поступил?"
        ),
        reply_markup=keyboard
    )


@dp.callback_query(lambda c: c.data == "form_commerce")
async def commerce_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Еще не оплатил учебу?", callback_data="commerce_not_paid")],
        [InlineKeyboardButton(text="Уже оплатил учебу?", callback_data="commerce_paid")]
    ])

    await callback_query.message.answer(
        text="Тебе нужно оплатить учебу, без этого не допустят к сессии",
        reply_markup=keyboard
    )


@dp.callback_query(lambda c: c.data == "commerce_not_paid")
async def not_paid_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сколько платить?", callback_data="payment_how_much")],
        [InlineKeyboardButton(text="Куда платить?", callback_data="payment_where")]
    ])

    await callback_query.message.answer(
        text="Смотри здесь, сколько платить и куда платить",
        reply_markup=keyboard
    )


@dp.callback_query(lambda c: c.data == "payment_how_much")
async def how_much_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=(
            "Смотри здесь: "
            "https://drive.google.com/file/d/1auxvX97briQk4Yzed-23yS1QyuAaSrKW/view?usp=sharing\n\n"
            "Найди в приказе свою специализацию (ее смотри в договоре на обучение), "
            "стоимость дели на 2, так как она указана за год обучения."
        )
    )


@dp.callback_query(lambda c: c.data == "payment_where")
async def where_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=(
            "Сайт для оплаты учебы: https://www.omgups.ru/payment/oplata-cherez-sberbank-onlayn/\n\n"
            "Реквизиты для оплаты обучения: https://www.omgups.ru/university/odro/novye-rekvizity/"
        )
    )


@dp.callback_query(lambda c: c.data in ["commerce_paid", "form_budget", "form_target"])
async def login_or_password_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получил логин пароль", callback_data="got_login")],
        [InlineKeyboardButton(text="Не получил логин пароль", callback_data="no_login")],
    ])

    await callback_query.message.answer(
        text=(
            "С 1 ноября ОмГУПС начнет высылать логин и пароль от портала на почту, которую ты указал при поступлении."
        ),
        reply_markup=keyboard
    )


# Не получил логин пароль
@dp.callback_query(lambda c: c.data == "no_login")
async def no_login_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=(
            "Напиши на почту odo@omgups.ru: «Добрый день, Ф.И.О. поступил на 1 курс специальность (указать свою),прошу выдать учетную запись для портала дистанционного обучения». После пиши нам https://vk.com/omgups_kontrolnay , чтобы мы тебе помогли с сессией"
        )
    )


# Получил логин пароль
@dp.callback_query(lambda c: c.data == "got_login")
async def got_login_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Буду делать сам", callback_data="do_self")],
        [InlineKeyboardButton(text="Нужна помощь", callback_data="need_help")],
        [InlineKeyboardButton(text="Нужна справка-вызов", callback_data="need_certificate")]
    ])

    await callback_query.message.answer(
        text=(
            "Сессия будет проходить здесь: https://dot.omgups.ru/ в дистанционном формате. В личном кабинете появятся задания, которые нужно будет выполнить и загрузить на портал."
        ),
        reply_markup=keyboard
    )


@dp.callback_query(lambda c: c.data == "do_self")
async def do_self_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Не понял, как делать", callback_data="dont_understand")],
        [InlineKeyboardButton(text="Есть вопросы по заданиям", callback_data="task_questions")]
    ])

    await callback_query.message.answer(
        text="Наверняка у тебя есть вопросы по сессии",
        reply_markup=keyboard
    )


# Не понял, как делать
@dp.callback_query(lambda c: c.data == "dont_understand")
async def dont_understand_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=(
            "Задай вопрос, и мы ответим тебе:\n"
            "Официальная группа ВКонтакте: https://vk.com/omgups_kontrolnay\n"
            "Официальная страница ВКонтакте: https://m.vk.com/id693153936\n"
            "Телефоны для связи: 89236706755 / 89136655213\n"
            "Наша почта: zakajirabotu@mail.ru\n"
            "Номер WhatsApp: 89136655213\n"
            "Офис: г. Омск, проспект Карла Маркса, 18к1, офис 211\n"
            "ПН-ПТ: 9:00-18:00\n"
            "СБ: 9:00-16:00\n"
            "Обед: 13:00-14:00"
        )
    )


# Есть вопросы по заданиям
@dp.callback_query(lambda c: c.data == "task_questions")
async def task_questions_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text="Ответы на часто задаваемые вопросы https://t.me/c/1504718431/237"
    )


# Нужна помощь
@dp.callback_query(lambda c: c.data == "need_help")
async def need_help_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text="Для заказа контрольных работ напиши нам в любой удобный для тебя мессенджер, и наш менеджер проконсультирует тебя по всем вопросам!\n"
             "Официальная группа ВКонтакте: https://vk.com/omgups_kontrolnay\n"
             "Официальная страница ВКонтакте: https://m.vk.com/id693153936\n"
             "Телефоны для связи: 89236706755 / 89136655213\n"
             "Почта: zakajirabotu@mail.ru\n"
             "Номер WhatsApp: 89136655213\n"
             "Оформление заказа: https://t.me/grandmaster55_bot\n"
             "Офис: г. Омск, проспект Карла Маркса, 18к1, офис 211\n"
             "ПН-ПТ 9:00-18:00\n"
             "СБ 9:00-16:00\n"
             "Обед: 13:00-14:00"
    )


# Нужна справка-вызов
@dp.callback_query(lambda c: c.data == "need_certificate")
async def need_certificate_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заполни заявление и отправь его на почту методисту",
                              callback_data="send_statement")],
        [InlineKeyboardButton(text="Или напиши сообщение методисту", callback_data="send_message_methodist")],
        [InlineKeyboardButton(text="Контакты методистов", callback_data="contact_methodist")]
    ])

    await callback_query.message.answer(
        text="Чтобы получить справку-вызов сделай следующее:",
        reply_markup=keyboard
    )


# Заполни заявление и отправь его на почту методисту
@dp.callback_query(lambda c: c.data == "send_message_methodist")
async def send_message_methodist_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=(
            "Добрый день, студент 1 курса группы 74 (указать свою специальность) ФИО,\n"
            "прошу выслать на электронную почту (указать свою эл. почту) справку-вызов для участия в сессии.\n"
            "Полное название организации: (указать)\n\n"
            "ВАЖНО!! В заявлении и сообщении нужно указать ПОЛНОЕ НАИМЕНОВАНИЕ ПРЕДПРИЯТИЯ, ГДЕ РАБОТАЕТЕ!"
        )
    )


# Заполни заявление и отправь его на почту методисту
@dp.callback_query(lambda c: c.data == "send_statement")
async def send_statement_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text="Форма заявления здесь: https://drive.google.com/file/d/1AiN_sskp1MxwW1kPAbpdPO0Z_GdlZDgl/view"
    )


# Контакты методистов
@dp.callback_query(lambda c: c.data == "contact_methodist")
async def contact_methodist_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=(
            "Если вы обучаетесь на специальности СЭ, ЛТ, ТМ, ваш методист:\n"
            "Баканова Елена Игоревна - телефон +7-3812-44-34-42, почта zfomgups-156-1@mail.ru\n\n"
            "Если вы обучаетесь на специальности БД, АТ, ОД, РС, СП, ТБ, ТЛ, ваш методист:\n"
            "Васильева Василиса Александровна - телефон +7-3812-44-34-79, почта zfomgups-155-1@mail.ru\n\n"
            "Если вы обучаетесь на специальности В, ГВ, ПВ, ТР, ЛЭ, ваш методист:\n"
            "Тимашкова Клавдия Дмитриевна - телефон +7-3812-44-34-42, почта zfomgups-156-2@mail.ru\n\n"
            "Если вы обучаетесь на специальности ТД, ЭБ, ИМ, ИП, ЛО, МО, СО, СИ, ТЛ, ФК, ПТ, НГ, ваш методист:\n"
            "Чешегорова Ольга Александровна - телефон +7-3812-44-34-79, почта zfomgups-155-2@mail.ru"
        )
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
