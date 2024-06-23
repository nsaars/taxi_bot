from aiogram.types import InlineKeyboardMarkup
from callbacks.crud_callbacks.settings_callbacks import *
from keyboards.inline.consts import InlineConstructor


def settings_menu_keyboard(**kwargs) -> InlineKeyboardMarkup:

    actions = [
        {"text": f"{'Запретить' if kwargs['allow_credits'] else 'Разрешить'} бронировать без баллов",
         "callback_data": SettingsUpdateCallbackData(variable='allow_credits', value=(not kwargs['allow_credits'])).pack()},
        {"text": "Назад", "callback_data": "crud_menu"}

    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)
