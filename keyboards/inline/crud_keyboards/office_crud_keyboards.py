from aiogram.types import InlineKeyboardMarkup
from callbacks.crud_callbacks.office_crud_callbacks import *
from keyboards.inline.consts import InlineConstructor
from typing import List, Dict, Optional


def office_menu_keyboard(role) -> InlineKeyboardMarkup:
    actions = []
    if role == 'admin':
        actions = [
            {"text": "Добавить офис", "callback_data": OfficeAddCallbackData().pack()}
        ]
    actions += [
        {"text": "Выбрать офис", "callback_data": OfficeChooseCallbackData().pack()},
        {"text": "Назад", "callback_data": "crud_menu"}
    ]
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)


def office_choose_keyboard(offices: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    actions = []
    for office in offices:
        actions.append({"text": office['title'], "callback_data": OfficeCallbackData(office=office['id']).pack()})

    actions.append({"text": "Назад", "callback_data": OfficeMenuCallbackData().pack()})
    schema = [1] * (len(offices) + 1)
    return InlineConstructor.create_kb(actions, schema)


def office_select_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Получить информацию о офисе", "callback_data": OfficeViewCallbackData().pack()},
        {"text": "Исправить информацию о офисе", "callback_data": OfficeEditCallbackData().pack()},
        {"text": "Удалить офис", "callback_data": OfficeRemoveCallbackData().pack()},
        {"text": "Назад", "callback_data": OfficeMenuCallbackData().pack()},
    ]
    schema = [1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def office_view_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Исправить информацию о офисе", "callback_data": OfficeEditCallbackData().pack()},
        {"text": "Назад", "callback_data": OfficeMenuCallbackData().pack()}
    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)


def office_edit_keyboard(role) -> InlineKeyboardMarkup:
    actions = []
    if role == 'admin':
        actions = [
            {"text": "Привязанный управляющий", "callback_data": OfficeEditFieldCallbackData(field="manager").pack()},
            {"text": "Адрес", "callback_data": OfficeEditFieldCallbackData(field="address").pack()},
            {"text": "Название", "callback_data": OfficeEditFieldCallbackData(field="title").pack()}
        ]
    actions += [

        {"text": "Подарки", "callback_data": OfficeEditFieldCallbackData(field="product").pack()},
        {"text": "Назад", "callback_data": OfficeChooseCallbackData().pack()}
    ]
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)


def office_edit_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": OfficeMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def office_add_keyboard(user: Optional[Dict[str, str]] = None, address: Optional[str] = None,
                        title: Optional[str] = None) -> InlineKeyboardMarkup:
    actions = [
        {"text": f"Управляющий: {user['telegram_username']}" if user else "Добавить управляющего",
         "callback_data": OfficeAddFieldCallbackData(field='manager').pack()},
        {"text": f"Адрес: {address}" if address else "Добавить адрес",
         "callback_data": OfficeAddFieldCallbackData(field='address').pack()},
        {"text": f"Название: {title}" if title else "Добавить название",
         "callback_data": OfficeAddFieldCallbackData(field='title').pack()},
        {"text": "Сохранить", "callback_data": OfficeSaveCallbackData().pack()},
        {"text": "Назад", "callback_data": OfficeMenuCallbackData().pack()}
    ]
    schema = [1, 1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def office_product_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Добавить подарок", "callback_data": OfficeChooseProductCallbackData(action='add').pack()},
        {"text": "Изменить количество", "callback_data": OfficeChooseProductCallbackData(action='update').pack()},
        {"text": "Удалить подарок", "callback_data": OfficeChooseProductCallbackData(action='remove').pack()},
        {"text": "Назад", "callback_data": OfficeEditCallbackData().pack()}
    ]
    schema = [1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def office_product_choose_keyboard(products: List[Dict[str, str]], action: str) -> InlineKeyboardMarkup:
    if action == 'add':
        callback_data = OfficeAddProductCallbackData
    elif action == 'remove':
        callback_data = OfficeRemoveProductCallbackData
    else:
        callback_data = OfficeUpdateProductCallbackData

    actions = []
    for product in products:
        actions.append({"text": product['title'], "callback_data": callback_data(product=product['id']).pack()})
    actions.append({"text": "Назад", "callback_data": OfficeEditFieldCallbackData(field="product").pack()})
    schema = [1] * (len(products) + 1)
    return InlineConstructor.create_kb(actions, schema)


def office_add_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": OfficeAddCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def office_remove_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": OfficeMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def office_back_to_keyboard(back_to: CallbackData) -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": back_to.pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)
