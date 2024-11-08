import asyncio
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import *

if __name__ == '__main__':
    tokens = ['6074471528:AAEz-tBGwiBoRrI7sd01lWMeVKi27Q5IkWo', '6324885383:AAG6t1M2ii1qLwBjEaxY7QMwW7MMt_sHIKw',
              '6318444504:AAEaOhDTL9smyxw_u5FAbE3ExhmjzMZfqAM']  # Ваши токены

    loop = asyncio.get_event_loop()

    bots = [Bot(token=token) for token in tokens]
    storages = [MemoryStorage() for _ in tokens]
    dps = [Dispatcher(bot, storage=storage) for bot, storage in zip(bots, storages)]

    # Регистрация обработчиков для каждого бота
    for dp in dps:
        dp.register_message_handler(start_command, commands=['start'], state=None)
        dp.register_message_handler(start_processing, commands=['processing'], state=None)
        dp.register_message_handler(stop_command, commands=['stop'], state=State.STARTED)
        dp.register_message_handler(db_start, commands=['db'], state=None)
        dp.register_message_handler(db_handle_message, state=State.STARTED_DB)
        dp.register_message_handler(db_document_message, state=[State.BASE, State.ADD],
                                    content_types=types.ContentType.DOCUMENT)
        dp.register_message_handler(clean_base_message, state=State.CLEAN)
        dp.register_message_handler(db_base_message, state=[State.BASE, State.ADD])

    tasks = [asyncio.ensure_future(dp.start_polling()) for dp in dps]
    loop.run_until_complete(asyncio.gather(*tasks))
