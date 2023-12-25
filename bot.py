from content.contents import message_dict, smile_dict
from content.keyboards import KeyBoards
from DataBase.databse import db_start, cmd_start_db

from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F


# Загрузка параметров конфигурации из файла .env
load_dotenv()
# Получаение токена
TOKEN = getenv("TOKEN")
# создание диспечера
dp = Dispatcher()
# инициализациябота
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


# Обработчик самой первой команды 'start'
@dp.message(CommandStart())
async def start_bot(message: Message):
    await cmd_start_db(message.from_user.id)
    await message.answer_sticker(smile_dict[2])
    await message.answer(f"{message.from_user.first_name}{message_dict[1]}{smile_dict[1]}", \
        reply_markup=KeyBoards.create_keyboard(smile_dict[3], smile_dict[4], smile_dict[5]))
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await message.answer(f"Вы авторизированны как АДМИН!", \
        reply_markup=KeyBoards.create_keyboard(smile_dict[3], smile_dict[4], smile_dict[5], smile_dict[6]))


# Обработчик выводит каталог товаров
@dp.message(F.text == smile_dict[3])
async def catalog_saler(message: Message):
    await message.answer(message_dict[4])


# Обработчик показывает корзину
@dp.message(F.text == smile_dict[4])
async def basket_saler(message: Message):
    await message.answer(message_dict[5])


# Обработчик выводит контакты для связи с продавцом
@dp.message(F.text == smile_dict[5])
async def contacts_saler(message: Message):
    await message.answer(message_dict[3])


# Обработчик выводит контакты для связи с продавцом
@dp.message(F.text == smile_dict[10])
async def contacts_saler(message: Message):
    await message.answer(f"{message.from_user.first_name}{message_dict[1]}{smile_dict[1]}", \
        reply_markup=KeyBoards.create_keyboard(smile_dict[3], smile_dict[4], smile_dict[5]))
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await message.answer(f"Вы авторизированны как АДМИН!", \
        reply_markup=KeyBoards.create_keyboard(smile_dict[3], smile_dict[4], smile_dict[5], smile_dict[6]))


# Обработчик выводит админ-меню
@dp.message(F.text == smile_dict[6])
async def admin_saler(message: Message):
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await message.answer(message_dict[6], \
            reply_markup=KeyBoards.create_keyboard(smile_dict[7], smile_dict[8], smile_dict[9], smile_dict[10]))
    else:
        await message.answer(message_dict[7])


# Функция инициализации и запуск бота и его базы данных 
async def main():
    await db_start()
    print("Бот успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())