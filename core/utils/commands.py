from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


# Хэндлер меню (синяя кнопочка слева - снизу).
async def set_commands(bot: Bot):
    commands: list = [
        BotCommand(
            command='start',
            description='Начало работы!'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
