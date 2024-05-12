"""
Модуль для работы с формами машины состояний FSM.

classes:
    Form_add: Содержит состояния для добавления товара в таблицу.
    Form_mailing: Содержит состояния для отправки массовой рассылки.
"""

from aiogram.fsm.state import State, StatesGroup


class Form_add(StatesGroup):
    """Cостояний FSM(добавление товаров)."""

    name = State()
    description = State()
    price = State()
    category = State()
    photo = State()


class Form_mailing(StatesGroup):
    """Cостояний FSM(рассылка оповещений)."""

    text = State()
