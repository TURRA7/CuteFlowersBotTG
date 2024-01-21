from ..content.contents import message_dict, smile_dict
from ..database.connectionDB import Tools
from core.keyboards.reply_inline import ReplyKeyBoards, InlineKeyBoards
from core.utils.commands import set_commands
from core.settings import settings

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Bot, types


# Определение состояний
class Form(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()


# Хэндлер комманды 'start'...
async def get_start(message: Message, bot: Bot):
    await message.answer_sticker(smile_dict[2])
    if message.from_user.id == settings.bots.admin_id:
        await message.answer(f"<b>{message.from_user.first_name}</b>{message_dict[1]}\
            ", reply_markup=ReplyKeyBoards.create_keyboard_reply(smile_dict[3],\
            smile_dict[5], smile_dict[6]))
    else:
        await message.answer(f"<b>{message.from_user.first_name}</b>{message_dict[1]}\
            {smile_dict[1]}", \
            reply_markup=ReplyKeyBoards.create_keyboard_reply(smile_dict[3],\
            smile_dict[5]))


# Хэндлер оповещения админа о запуске бота.
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text=message_dict[16])


# Хэндлер оповещения админа об остановке бота.
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text=message_dict[17])


# Обработчик выводит контакты для связи с продавцом.
async def contacts_saler(message: Message):
    await message.answer(message_dict[3])
    await message.answer(message_dict[18])
    await message.answer(message_dict[19])


# Обработчик выводит админ-меню.
async def admin_saler(message: Message):
    await message.answer(message_dict[6], \
        reply_markup=ReplyKeyBoards.create_keyboard_reply(smile_dict[7], \
        smile_dict[10]))


# Обработчик выводит стартовое меню.
async def main_menu(message: Message):
    await message.answer_sticker(smile_dict[2])
    if message.from_user.id == settings.bots.admin_id:
        await message.answer(f"<b>{message.from_user.first_name}</b>{message_dict[1]}\
            ", reply_markup=ReplyKeyBoards.create_keyboard_reply(smile_dict[3],\
            smile_dict[5], smile_dict[6]))
    else:
        await message.answer(f"<b>{message.from_user.first_name}</b>{message_dict[1]}\
            {smile_dict[1]}", \
            reply_markup=ReplyKeyBoards.create_keyboard_reply(smile_dict[3],\
            smile_dict[5]))


# FSM - Начало, ввод названия товара.
async def add_item(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer(message_dict[9])


# FSM - Ввод описания товара.
async def add_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.description)
    await message.answer(message_dict[13])


# FSM - Ввод цены товара.
async def add_item_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Form.price)
    await message.answer(message_dict[14])


# FSM - Добавление фото товара.
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Form.photo)
    await message.answer(message_dict[15])


# FSM - Контрольная обработка, добавление в БД.
async def add_item_photo(message: Message, state: FSMContext):
    photo_file_id: str = message.photo[-1].file_id
    data: dict = await state.get_data()
    await Tools.add_item(name=str(data['name']), description=str(data['description']), price=int(data['price']), photo=str(photo_file_id))
    await message.answer(message_dict[12])
    await state.clear()
        

# Обработчик выводит каталог товаров.
async def item_catalog(message: Message):
    items: dict = await Tools.select_item()
    if not len(items) >= 1:
        await message.answer(message_dict[4])
    for item in await Tools.select_item():
            text: list = [item.name, item.description, str(item.price)+'p.']
            if message.from_user.id == settings.bots.admin_id:
                await message.answer_photo(item.photo,
                    '\n'.join(text), reply_markup=InlineKeyBoards.create_keyboard_inline('Удалить', f"delete_item:{item.id}"))
            else:
                await message.answer_photo(item.photo,
                    '\n'.join(text))


# Обработчик кнопки "УДАЛИТЬ", удаляет товар и выводит сообщение об этом.
async def delete_item(callback_query: types.CallbackQuery, bot: Bot):
    item_id: int = int(callback_query.data.split(':')[1])
    await Tools.del_item(item_id)
    await bot.send_message(callback_query.from_user.id, "Товар успешно удален")