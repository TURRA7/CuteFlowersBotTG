from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram import types

# Создаем inline-клавиатуру с кнопкой "Удалить"


# Класс по Reply клавиатуре.
class ReplyKeyBoards:
    def __init__(self):
        pass

    # Метод создаёт клавиатуру с преданым колличеством кнопопк.
    @staticmethod
    def create_keyboard_reply(*buttons):
        kb: list = [[types.KeyboardButton(text=button,)] for button in buttons]
        keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
        return keyboard


# Класс по Inline клавиатуре.
class InlineKeyBoards:
    def __init__(self):
        pass

    @staticmethod
    def create_keyboard_inline(text, callbacks):
        links_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=text, callback_data=callbacks)
                ]
            ]
        )
        return links_kb
        
        