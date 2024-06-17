from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup
from callbacks.crud_callbacks.manager_crud_callbacks import (
    ManagerMenuCallbackData,
    ManagerViewCallbackData,
    ManagerEditCallbackData,
    ManagerEditFieldCallbackData,
    ManagerChooseCallbackData,
    ManagerAddCallbackData,
    ManagerSaveCallbackData,
    ManagerAddFieldCallbackData,
    ManagerAddOfficeCallbackData,
    ManagerRemoveCallbackData, ManagerChooseOfficeCallbackData, ManagerRemoveOfficeCallbackData, ManagerCallbackData
)
from keyboards.inline.consts import InlineConstructor


def manager_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Добавить менеджера", "callback_data": ManagerAddCallbackData().pack()},
        {"text": "Выбрать менеджера", "callback_data": ManagerChooseCallbackData().pack()},
        {"text": "Назад", "callback_data": "crud_menu"}
    ]
    schema = [1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def manager_choose_keyboard(managers_users: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    actions = []
    for manager_user in managers_users:
        actions.append({"text": manager_user['user']['telegram_username'], "callback_data": ManagerCallbackData(manager=manager_user['manager']['id']).pack()})

    actions.append({"text": "Назад", "callback_data": ManagerMenuCallbackData().pack()})
    schema = [1] * (len(managers_users) + 1)
    return InlineConstructor.create_kb(actions, schema)



def manager_select_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Получить информацию о менеджере", "callback_data": ManagerViewCallbackData().pack()},
        {"text": "Удалить менеджера", "callback_data": ManagerRemoveCallbackData().pack()},
        {"text": "Назад", "callback_data": "crud_menu"},
    ]
    schema = [1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def manager_view_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": ManagerMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def manager_edit_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Офис", "callback_data": ManagerEditFieldCallbackData(field="office").pack()},
        {"text": "Назад", "callback_data": ManagerMenuCallbackData().pack()}
    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)


def manager_edit_office_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Добавить офис", "callback_data": ManagerChooseOfficeCallbackData(action="add").pack()},
        {"text": "Назад", "callback_data": ManagerMenuCallbackData().pack()}
    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)


def manager_edit_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": ManagerMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def manager_add_keyboard(user=None) -> InlineKeyboardMarkup:
    actions = [
        {"text": f"Пользователь: {user['telegram_username']}" if user else "Добавить пользователя",
         "callback_data": ManagerAddFieldCallbackData(field='user').pack()},
        {"text": "Сохранить", "callback_data": ManagerSaveCallbackData().pack()},
        {"text": "Назад", "callback_data": ManagerMenuCallbackData().pack()}
    ]
    schema = [1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def manager_add_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": ManagerAddCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def manager_remove_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": ManagerMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def manager_office_list_keyboard(offices, status) -> InlineKeyboardMarkup:
    if status == 'add':
        callback_data = ManagerAddOfficeCallbackData
    else:
        callback_data = ManagerRemoveOfficeCallbackData

    actions = []
    for office in offices:
        actions.append({"text": office['title'], "callback_data": callback_data(office=office['id']).pack()})
    actions += [
        {"text": "Назад", "callback_data": ManagerEditCallbackData(field='office').pack()}
    ]
    schema = [1] * (len(offices) + 1)
    return InlineConstructor.create_kb(actions, schema)


def manager_back_to_keyboard(back_to) -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": back_to().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)
