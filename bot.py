from DataBase.databse import async_main, Tools, Product
from content.contents import message_dict, smile_dict
from content.keyboards import KeyBoards


from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import sys

from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
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
# Добавление роутера
router = Router()


# Определение состояний
class Form(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()



# Обработчик самой первой команды 'start'
@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer_sticker(smile_dict[2])
    await message.answer(f"{message.from_user.first_name}{message_dict[1]}\
        {smile_dict[1]}", reply_markup=KeyBoards.create_keyboard(smile_dict[3],\
        smile_dict[4], smile_dict[5]))
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await message.answer(f"Вы авторизированны как АДМИН!", \
        reply_markup=KeyBoards.create_keyboard(smile_dict[3], smile_dict[5], \
        smile_dict[6]))


# Обработчик выводит каталог товаров
@router.message(F.text == smile_dict[3])
async def catalog_saler(message: Message):
    await message.answer(message_dict[4])

'''
# Обработчик показывает корзину
@router.message(F.text == smile_dict[4])
async def basket_saler(message: Message):
'''


# Обработчик выводит контакты для связи с продавцом
@router.message(F.text == smile_dict[5])
async def contacts_saler(message: Message):
    await message.answer(message_dict[3])


# Обработчик выводит контакты для связи с продавцом
@router.message(F.text == smile_dict[10])
async def contacts_saler(message: Message):
    await message.answer(f"{message.from_user.first_name}{message_dict[1]}\
        {smile_dict[1]}", reply_markup=KeyBoards.create_keyboard(smile_dict[3],\
        smile_dict[4], smile_dict[5]))
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await message.answer(message_dict[8], \
        reply_markup=KeyBoards.create_keyboard(smile_dict[3], smile_dict[5],\
        smile_dict[6]))


# Обработчик выводит админ-меню
@router.message(F.text == smile_dict[6])
async def admin_saler(message: Message):
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await message.answer(message_dict[6], \
            reply_markup=KeyBoards.create_keyboard(smile_dict[7], \
            smile_dict[8], smile_dict[9], smile_dict[10]))
    else:
        await message.answer(message_dict[7])


# Обработчик выводит контакты для связи с продавцом
@router.message(F.text == smile_dict[7])
async def add_item(message: Message, state: FSMContext):
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await state.set_state(Form.name)
        await message.answer(message_dict[9])
    else:
        await message.answer(message_dict[7])


@router.message(Form.name)
async def add_item_name(message: Message, state: FSMContext):
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await state.update_data(name=message.text)
        await state.set_state(Form.description)
        await message.answer(message_dict[13])


@router.message(Form.description)
async def add_item_name(message: Message, state: FSMContext):
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await state.update_data(description=message.text)
        await state.set_state(Form.price)
        await message.answer(message_dict[14])


@router.message(Form.price)
async def add_item_name(message: Message, state: FSMContext):
    if message.from_user.id == int(getenv('ADMIN_ID')):
        await state.update_data(price=message.text)
        await state.set_state(Form.photo)
        await message.answer(message_dict[15])


@router.message(Form.photo, F.photo)
async def add_item_name(message: Message, state: FSMContext):
    if message.from_user.id == int(getenv('ADMIN_ID')):
        photo_file_id = message.photo[-1].file_id
        data = await state.get_data()
        await state.clear()

        formatted_text = {key:value for (key,value) in data.items()}

        await Tools.add_item(formatted_text['name'], \
            formatted_text['description'], formatted_text['price'],\
            photo_file_id)
        await message.answer(message_dict[12])

 
# Функция инициализации и запуск бота и его базы данных 
async def main():
    await async_main()
    print(message_dict[11])
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")