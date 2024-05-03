import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F

from core.handlers.basic import (
    get_start, start_bot, stop_bot,
    contacts_saler, admin_saler, main_menu,
    add_item, add_item_name, add_item_description,
    add_item_price, Form, add_item_photo,
    delete_item, add_item_category
)
from core.content.contents import emoticons
from core.database.ADataBase import DataBaseTools
from settings import settings


# Создание логгера
logger = logging.getLogger('log_app.log')
logger.setLevel(logging.DEBUG)
# Создание обработчика консоли и установка уровеня отладки
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Создание форматтера
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Добавить форматтер в ch
ch.setFormatter(formatter)
# Добавлении ротации логов
file_handler = RotatingFileHandler('log_app.log',
                                   maxBytes=1024 * 1024,
                                   backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# Добавить ch в логгер, создание ротации
logger.addHandler(ch)
logger.addHandler(file_handler)


async def start():
    """Функция инициации и запуска бота."""
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    # Объект класса Диспечер
    dp = Dispatcher()

    # Регистрация хэндлеров(Общие):
    dp.message.register(get_start, Command("start"))
    dp.message.register(contacts_saler, F.text == emoticons[5])
    dp.message.register(admin_saler, F.text == emoticons[6],
                        F.from_user.id == settings.bots.admin_id)
    dp.message.register(main_menu, F.text == emoticons[10])
    dp.callback_query.register(delete_item,
                               lambda c: c.data.startswith('delete_item:'))

    # Регистрация хэндлеров(FSM):
    dp.message.register(add_item, F.text == emoticons[7],
                        F.from_user.id == settings.bots.admin_id)
    dp.message.register(add_item_name, Form.name,
                        F.from_user.id == settings.bots.admin_id)
    dp.message.register(add_item_description, Form.description,
                        F.from_user.id == settings.bots.admin_id)
    dp.message.register(add_item_price, Form.price,
                        F.from_user.id == settings.bots.admin_id)
    dp.message.register(add_item_category, Form.category,
                        F.from_user.id == settings.bots.admin_id)
    dp.message.register(add_item_photo, Form.photo,
                        F.from_user.id == settings.bots.admin_id)

    # Регистрация хэндлеров(Старт/остановка бота):
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    tools = DataBaseTools()
    tools.create_table()

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
