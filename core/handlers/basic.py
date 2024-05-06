"""Модуль обработчиков aiogram3."""

from ..content.contents import messages, emoticons, values
from core.keyboards.reply_inline import ReplyKeyBoards, InlineKeyBoards
from core.utils.commands import set_commands
from ..database.ADataBase import DataBaseTools
from settings import settings

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Bot, types


class Form(StatesGroup):
    """Класс определения состояний, для машины состояний FSM."""

    name = State()
    description = State()
    price = State()
    category = State()
    photo = State()


async def get_start(message: Message):
    """Обработчик команды stsrt."""
    await message.answer_sticker(emoticons[2])
    if message.from_user.id == settings.bots.admin_id:
        await message.answer(
            f"<b>{message.from_user.first_name}</b>{messages[1]}",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[3],
                                                              emoticons[5],
                                                              emoticons[6]))
    else:
        await message.answer(
            f"<b>{message.from_user.first_name}</b>{messages[1]}",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[3],
                                                              emoticons[5]))


async def start_bot(bot: Bot):
    """Оповещения для админа(об старте бота)."""
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text=messages[16])


async def stop_bot(bot: Bot):
    """Оповещения для админа(об остановки бота)."""
    await bot.send_message(settings.bots.admin_id, text=messages[17])


async def contacts_saler(message: Message):
    """Вывод контактов продавца."""
    await message.answer(messages[3])
    await message.answer(messages[18])
    await message.answer(messages[19])


async def admin_saler(message: Message):
    """Вывод админ меню."""
    await message.answer(
        messages[6],
        reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[7],
                                                          emoticons[10]))


async def main_menu(message: Message):
    """Вывод стартового меню."""
    await message.answer_sticker(emoticons[2])
    if message.from_user.id == settings.bots.admin_id:
        await message.answer(
            f"<b>{message.from_user.first_name}</b>{messages[1]}",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[3],
                                                              emoticons[5],
                                                              emoticons[6]))
    else:
        await message.answer(
            f"<b>{message.from_user.first_name}</b>{messages[1]}",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[3],
                                                              emoticons[5]))


async def add_item(message: Message, state: FSMContext):
    """Этап: 1(FSM) - ввод названия товара."""
    await state.set_state(Form.name)
    await message.answer(messages[9])


async def add_item_name(message: Message, state: FSMContext):
    """Этап: 2(FSM) - ввод описания товара."""
    await state.update_data(name=message.text)
    await state.set_state(Form.description)
    await message.answer(messages[13])


async def add_item_description(message: Message, state: FSMContext):
    """Этап: 3(FSM) - ввод цены товара."""
    await state.update_data(description=message.text)
    await state.set_state(Form.price)
    await message.answer(messages[14])


async def add_item_price(message: Message, state: FSMContext):
    """Этап: 4(FSM) - ввод категории товара."""
    await state.update_data(price=message.text)
    await state.set_state(Form.category)
    await message.answer(messages[20])


async def add_item_category(message: Message, state: FSMContext):
    """Этап: 5(FSM) - добавление фото товара."""
    await state.update_data(category=message.text)
    await state.set_state(Form.photo)
    await message.answer(messages[15])


async def add_item_photo(message: Message, state: FSMContext):
    """Этап: 6(FSM) - контрольная обработка, добавление в базу данных."""
    photo_file_id: str = message.photo[-1].file_id
    data: dict = await state.get_data()

    tools = DataBaseTools()
    tools.insert_item("goods", title=str(data['name']),
                      description=str(data['description']),
                      price=int(data['price']),
                      category=int(data['category']),
                      photo=str(photo_file_id))
    await message.answer(messages[12])
    await state.clear()
    await message.answer(
        messages[22],
        reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[7],
                                                          emoticons[10]))


async def item_catalog(message: Message):
    """Вывод категорий каталога."""
    await message.answer(messages[21],
                         reply_markup=ReplyKeyBoards.create_keyboard_reply(
                             emoticons[11],
                             emoticons[12],
                             emoticons[13],
                             emoticons[14]))


async def item_category(message: Message):
    """Выводит выбраную категорию товара."""
    key = 0
    for key, value in emoticons.items():
        if value == message.text:
            key = key
            break
    tools = DataBaseTools()
    items: tuple = tools.fetch_all_items(values[key])
    if not len(items) >= 1:
        await message.answer(messages[23])
    for item in items:
        text: list = [item[1], item[2], f"{str(item[3])}р."]
        await message.answer_photo(
            item[5], "\n".join(text),
            reply_markup=InlineKeyBoards.create_keyboard_inline(
                'Удалить', f"delete_item:{item[0]}"))


async def delete_item(callback_query: types.CallbackQuery, bot: Bot):
    """Обработчик кнопки 'удалить', удаляет выбраный товар из базы данных."""
    item_id: int = int(callback_query.data.split(':')[1])
    tools = DataBaseTools()
    tools.delete_item(item_id)
    await bot.send_message(callback_query.from_user.id, "Товар успешно удален")
