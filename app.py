"""
Модуль исполнительного файла.

Данный модуль, содержит логирование.

function:
    start: Функция инициации и запуска бота.
"""

import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F

from core.handlers.basic import (
    get_start, start_bot, stop_bot,
    contacts_menu, admin_menu, main_menu,
    add_item, add_item_name, add_item_description,
    add_item_price, add_item_photo,
    delete_item, add_item_category, item_catalog,
    item_category, buy_item, start_mailing, send_mailing,
)
from core.forms_state.form_bot import Form_add, Form_mailing
from core.content.contents import emoticons
from core.database.ADataBase import DataBaseTools
from core.log_mod import Logger

# Создание логгера
db_logger = Logger("log_app.log")
logger = db_logger.get_logger()


async def start():
    """Функция инициации и запуска бота."""
    bot = Bot(token=os.getenv("TOKEN"), parse_mode='HTML')
    # Объект класса Диспечер
    dp = Dispatcher()

    admin_id = int(os.getenv('ADMIN_ID'))

    # Регистрация хэндлеров(Общие):
    dp.message.register(get_start, Command("start"))
    dp.message.register(contacts_menu, F.text == emoticons[5])
    dp.message.register(admin_menu, F.text == emoticons[6],
                        F.from_user.id == admin_id)
    dp.message.register(main_menu, F.text == emoticons[10])
    dp.callback_query.register(delete_item,
                               lambda c: c.data.startswith('delete_item:'))
    dp.message.register(item_catalog, F.text == emoticons[3])
    dp.message.register(item_category, F.text.in_({emoticons[11],
                                                   emoticons[12],
                                                   emoticons[13],
                                                   emoticons[14]}))
    dp.callback_query.register(buy_item,
                               lambda c: c.data.startswith('buy_item:'))

    # Регистрация хэндлеров(FSM - добавление товаров.):
    dp.message.register(add_item, F.text == emoticons[7],
                        F.from_user.id == admin_id)
    dp.message.register(add_item_name, Form_add.name,
                        F.from_user.id == admin_id)
    dp.message.register(add_item_description, Form_add.description,
                        F.from_user.id == admin_id)
    dp.message.register(add_item_price, Form_add.price,
                        F.from_user.id == admin_id)
    dp.message.register(add_item_category, Form_add.category,
                        F.from_user.id == admin_id)
    dp.message.register(add_item_photo, Form_add.photo,
                        F.from_user.id == admin_id)

    # Регистрация хэндлеров(FSM - рассылка.):
    dp.message.register(start_mailing, F.text == emoticons[15],
                        F.from_user.id == admin_id)
    dp.message.register(send_mailing, Form_mailing.text,
                        F.from_user.id == admin_id)

    # Регистрация хэндлеров(Старт/остановка бота):
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        # Создание таблиц в базу данных.
        tools = DataBaseTools()
        tools.create_table()
        # Запуск бота в режиме start_polling.
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
