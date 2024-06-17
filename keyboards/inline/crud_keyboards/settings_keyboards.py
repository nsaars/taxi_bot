from aiogram.types import InlineKeyboardMarkup
from callbacks.crud_callbacks.settings_callbacks import *
from keyboards.inline.consts import InlineConstructor


def settings_menu_keyboard(allow_credits: bool) -> InlineKeyboardMarkup:
    actions = [
        {"text": f"{'Запретить' if allow_credits else 'Разрешить'} бронировать без баллов",
         "callback_data": SettingsUpdateCallbackData(variable='allow_credits', value=(not allow_credits)).pack()},
        {"text": "Назад", "callback_data": "crud_menu"}

    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)
