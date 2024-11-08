from aiogram import Bot
import asyncio

bot_token = '6324885383:AAG6t1M2ii1qLwBjEaxY7QMwW7MMt_sHIKw'
bot = Bot(token=bot_token)


async def check_user_existence(username):
    user = await bot.get_chat(username)
    print(f"Пользователь с ником {user.username} существует.")


async def main():
    await check_user_existence('elaman2002')
    await bot.close()  # Закрытие сеанса клиента


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
