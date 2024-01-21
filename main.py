from core.handlers.basic import get_start, start_bot, stop_bot, contacts_saler
from core.handlers.basic import admin_saler, main_menu, add_item, add_item_name
from core.handlers.basic import add_item_description, add_item_price, Form
from core.handlers.basic import add_item_photo, item_catalog, delete_item
from core.content.contents import message_dict, smile_dict
from core.database.connectionDB import Tools, async_main
from core.settings import settings

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F


# Функция запуска бота...
async def start():
	# Подключение логгирования:
	logging.basicConfig(level=logging.INFO,
						format="%(asctime)s - [%(levelname)s] - $(name)s - "
								"(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
						)
	# Объект класса БОТ
	bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
	# Объект класса Диспечер
	dp = Dispatcher()

	# Регистрация хэндлеров(Общие):
	dp.message.register(get_start, Command("start"))
	dp.message.register(contacts_saler, F.text == smile_dict[5])
	dp.message.register(admin_saler, F.text == smile_dict[6], F.from_user.id == settings.bots.admin_id)
	dp.message.register(main_menu, F.text == smile_dict[10])
	dp.message.register(item_catalog, F.text == smile_dict[3])
	dp.callback_query.register(delete_item, lambda c: c.data.startswith('delete_item:'))

	# Регистрация хэндлеров(FSM):
	dp.message.register(add_item, F.text == smile_dict[7], F.from_user.id == settings.bots.admin_id)
	dp.message.register(add_item_name, Form.name, F.from_user.id == settings.bots.admin_id)
	dp.message.register(add_item_description, Form.description, F.from_user.id == settings.bots.admin_id)
	dp.message.register(add_item_price, Form.price, F.from_user.id == settings.bots.admin_id)
	dp.message.register(add_item_photo, Form.photo, F.photo, F.from_user.id == settings.bots.admin_id)

	# Регистрация хэндлеров(Старт/остановка бота):
	dp.startup.register(start_bot)
	dp.shutdown.register(stop_bot)

	try:
		# Вызов бота
		await async_main()
		await dp.start_polling(bot)
	finally:
		await bot.session.close()


if __name__ == "__main__":
	asyncio.run(start())