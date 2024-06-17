from aiogram.types import InlineKeyboardMarkup
from callbacks.crud_callbacks.driver_crud_callbacks import (
    DriverCrudMenuCallbackData,
    DriverViewCallbackData,
    DriverEditCallbackData,
    DriverEditFieldCallbackData,
    DriverChooseCallbackData
)
from keyboards.inline.consts import InlineConstructor


def driver_choose_keyboard(back_to='crud_menu') -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": back_to}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def driver_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Получить информацию о водителе", "callback_data": DriverViewCallbackData().pack()},
        {"text": "Исправить информацию о водителе", "callback_data": DriverEditCallbackData().pack()},
        {"text": "Назад", "callback_data": DriverChooseCallbackData().pack()},
    ]
    schema = [1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def driver_view_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Исправить информацию о водителе", "callback_data": DriverEditCallbackData().pack()},
        {"text": "Назад", "callback_data": DriverCrudMenuCallbackData().pack()}
    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)


def driver_edit_keyboard(is_blocked: bool, trusted: bool) -> InlineKeyboardMarkup:
    actions = [
        {"text": "Количество баллов", "callback_data": DriverEditFieldCallbackData(field="scores").pack()},
        {"text": "Разблокировать" if is_blocked else "Заблокировать", "callback_data": DriverEditFieldCallbackData(field="is_blocked").pack()},
        {"text": "Запретить бронировать без баллов" if trusted else "Разрешить бронировать без баллов",
         "callback_data": DriverEditFieldCallbackData(field="trusted").pack()},
        {"text": "Назад", "callback_data": DriverCrudMenuCallbackData().pack()}
    ]
    schema = [1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def driver_edit_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": DriverCrudMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)
