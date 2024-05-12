"""
Модуль содержит обработчики(хендлеры aiogram3).

Данный модуль, содержит логирование.

function:
get_start: Обработчик команды /start.
start_bot: Оповещает админа, об старте(включении) бота.
stop_bot: Оповещает админа, об остановке(выключении) бота.
contacts_menu: Обрабатывает вывод контактов по нажатию кнопки.
admin_menu: Обрабатывает вывод админ меню по нажатию кнопки.
main_menu: Обрабатывает вывод главного меню по нажатию кнопки.
add_item: Этап: 1(FSM) - ввод названия товара.
add_item_name: Этап: 2(FSM) - ввод описания товара.
add_item_description: Этап: 3(FSM) - ввод цены товара.
add_item_price: Этап: 4(FSM) - ввод категории товара.
add_item_category: Этап: 5(FSM) - добавление фото товара.
add_item_photo: Этап: 6(FSM) - контрольная обработка,
добавление в базу данных.
item_catalog: Обрабатывает вывод категорий каталога.
item_category: Обрабатывает вывод выбранной категории товара.
delete_item: Обработчик кнопки 'удалить', удаляет выбранный товар
из базы данных.
buy_item: Обработчик кнопки 'Купить', делает заявку на заказ.
start_mailing: Этап: 1(FSM) - ввод текста рассылки.
send_mailing: Этап: 2(FSM) - отправка.
"""

import pytz
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Bot, types

from ..content.contents import messages, emoticons, values
from core.keyboards.reply_inline import ReplyKeyBoards, InlineKeyBoards
from core.utils.commands import set_commands
from ..database.ADataBase import DataBaseTools
from ..forms_state.form_bot import Form_add, Form_mailing
from settings import settings
from ..log_mod import Logger


# Создание логгера
db_logger = Logger("log_basic.log")
logger = db_logger.get_logger()


async def get_start(message: Message):
    """Обработчик команды stsrt."""
    await message.answer_sticker(emoticons[2])
    tools = DataBaseTools()
    items = tools.fetch_all_items("users", "id_user")
    if message.from_user.id not in items:
        tools.insert_item(
            "users", name=message.from_user.username,
            id_user=message.from_user.id)
        logger.info("Пользователь %s добавлен!", message.from_user.username)
    elif message.from_user.id in items:
        logger.info("Пользователь %s уже есть в базе!",
                    message.from_user.username)
    else:
        logger.info("Ошибка добавления пользователя!")

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
    logger.info("Бот запущен!")
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text=messages[16])


async def stop_bot(bot: Bot):
    """Оповещения для админа(об остановки бота)."""
    logger.info("Бот Остановлен!")
    await bot.send_message(settings.bots.admin_id, text=messages[17])


async def contacts_menu(message: Message):
    """Вывод контактов продавца."""
    await message.answer(messages[3])
    await message.answer(messages[18])
    await message.answer(messages[19])


async def admin_menu(message: Message):
    """Вывод админ меню."""
    await message.answer(
        messages[6],
        reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[7],
                                                          emoticons[10],
                                                          emoticons[15]))


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
    await state.set_state(Form_add.name)
    await message.answer(messages[9])


async def add_item_name(message: Message, state: FSMContext):
    """Этап: 2(FSM) - ввод описания товара."""
    await state.update_data(name=message.text)
    await state.set_state(Form_add.description)
    await message.answer(messages[13])


async def add_item_description(message: Message, state: FSMContext):
    """Этап: 3(FSM) - ввод цены товара."""
    await state.update_data(description=message.text)
    await state.set_state(Form_add.price)
    await message.answer(messages[14])


async def add_item_price(message: Message, state: FSMContext):
    """Этап: 4(FSM) - ввод категории товара."""
    await state.update_data(price=message.text)
    await state.set_state(Form_add.category)
    await message.answer(messages[20])


async def add_item_category(message: Message, state: FSMContext):
    """Этап: 5(FSM) - добавление фото товара."""
    await state.update_data(category=message.text)
    await state.set_state(Form_add.photo)
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
                             emoticons[14],
                             emoticons[10]))


async def item_category(message: Message):
    """Выводит выбранную категорию товара."""
    key = 0
    for key, value in emoticons.items():
        if value == message.text:
            key = key
            break
    tools = DataBaseTools()
    items: tuple = tools.fetch_all_items_cat("goods", values[key])
    if not len(items) >= 1:
        await message.answer(messages[23])
    for item in items:
        text: list = [item[1], item[2], f"{str(item[3])}р."]
        if not message.from_user.id == settings.bots.admin_id:
            await message.answer_photo(
                item[5], "\n".join(text),
                reply_markup=InlineKeyBoards.create_keyboard_inline(
                    'Купить', f"buy_item:{item[0]}"))
        else:
            await message.answer_photo(
                    item[5], "\n".join(text),
                    reply_markup=InlineKeyBoards.create_keyboard_inline(
                        'Удалить', f"delete_item:{item[0]}"))


async def delete_item(callback_query: types.CallbackQuery, bot: Bot):
    """Обработчик кнопки 'удалить', удаляет выбраный товар из базы данных."""
    item_id: int = int(callback_query.data.split(':')[1])
    tools = DataBaseTools()
    tools.delete_item(item_id)
    await bot.send_message(callback_query.from_user.id,
                           "Товар успешно удален!")


async def buy_item(callback_query: types.CallbackQuery, bot: Bot):
    """Обработчик кнопки 'Купить', делает заявку на заказ."""
    item_id: int = int(callback_query.data.split(':')[1])
    tools = DataBaseTools()
    items = await tools.select_item_id(item_id)

    utc_timezone = pytz.utc
    utc_time = datetime.now(utc_timezone)
    time = utc_time.astimezone(pytz.timezone('EET'))
    time = time.strftime('%Y-%m-%d %H:%M:%S')

    text = ["Заявка:", f"Название: {items[1]}", f"Описание: {items[2]}",
            f"Цена: {items[3]}", f"Время и дата: {time}",
            f'https://t.me/{callback_query.from_user.username}']
    await bot.send_photo(settings.bots.admin_id, photo=items[5],
                         caption="\n".join(text))
    await bot.send_message(callback_query.from_user.id,
                           "Ожидайте, с вами свяжется продавец!")


async def start_mailing(message: Message, state: FSMContext):
    """Этап: 1(FSM) - ввод текста рассылки."""
    await state.set_state(Form_mailing.text)
    await message.answer(emoticons[16])


async def send_mailing(message: Message, state: FSMContext, bot: Bot):
    """Этап: 2(FSM) - отправка."""
    await state.update_data(text=message.text)
    data: dict = await state.get_data()
    text_mailing = str(data['text'])

    tools = DataBaseTools()
    users = tools.fetch_all_items("users", "id_user")
    for user in users:
        await bot.send_message(str(user), text_mailing, parse_mode=None)

    logger.info("Рассылка с сообзением: '%s' сделана пользователям: %s",
                text_mailing, users)

    await state.clear()
    await message.answer(
        messages[22],
        reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[7],
                                                          emoticons[10],
                                                          emoticons[15]))
