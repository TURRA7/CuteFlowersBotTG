from aiogram.types import ReplyKeyboardMarkup
from aiogram import Bot, Dispatcher, Router, types


class KeyBoards:  
    def __init__(self):
        pass

    @staticmethod
    def create_keyboard(*buttons):
        kb = [[types.KeyboardButton(text=button)] for button in buttons]
        keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
        return keyboard