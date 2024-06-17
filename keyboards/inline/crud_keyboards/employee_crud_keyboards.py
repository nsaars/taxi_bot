from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup
from callbacks.crud_callbacks.employee_crud_callbacks import (
    EmployeeCrudMenuCallbackData,
    EmployeeViewCallbackData,
    EmployeeEditCallbackData,
    EmployeeEditFieldCallbackData,
    EmployeeChooseCallbackData,
    EmployeeAddCallbackData,
    EmployeeSaveCallbackData,
    EmployeeAddFieldCallbackData,
    EmployeeAddOfficeCallbackData, EmployeeEditOfficeCallbackData, EmployeeRemoveCallbackData, EmployeeCallbackData
)
from keyboards.inline.consts import InlineConstructor


def employee_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Добавить сотрудника", "callback_data": EmployeeAddCallbackData().pack()},
        {"text": "Выбрать сотрудника", "callback_data": EmployeeChooseCallbackData().pack()},
        {"text": "Назад", "callback_data": "crud_menu"}
    ]
    schema = [1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def employee_choose_keyboard(employees_users: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    actions = []
    for employee_user in employees_users:
        actions.append({"text": employee_user['user']['telegram_username'], "callback_data": EmployeeCallbackData(employee=employee_user['employee']['id']).pack()})

    actions.append({"text": "Назад", "callback_data": EmployeeCrudMenuCallbackData().pack()})
    schema = [1] * (len(employees_users) + 1)
    return InlineConstructor.create_kb(actions, schema)


def employee_select_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Получить информацию о сотруднике", "callback_data": EmployeeViewCallbackData().pack()},
        {"text": "Исправить информацию о сотруднике", "callback_data": EmployeeEditCallbackData().pack()},
        {"text": "Удалить сотрудника", "callback_data": EmployeeRemoveCallbackData().pack()},
        {"text": "Назад", "callback_data": "crud_menu"},
    ]
    schema = [1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def employee_view_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Исправить информацию о сотруднике", "callback_data": EmployeeEditCallbackData().pack()},
        {"text": "Назад", "callback_data": EmployeeCrudMenuCallbackData().pack()}
    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)


def employee_edit_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Привязанный офис", "callback_data": EmployeeEditFieldCallbackData(field="office").pack()},
        {"text": "Назад", "callback_data": EmployeeCrudMenuCallbackData().pack()}
    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)


def employee_edit_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": EmployeeCrudMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def employee_add_keyboard(user=None, office=None) -> InlineKeyboardMarkup:
    actions = [
        {"text": f"Пользователь: {user['telegram_username']}" if user else "Добавить пользователя",
         "callback_data": EmployeeAddFieldCallbackData(field='user').pack()},
        {"text": f"Офис: {office['title']}" if office else "Добавить офис",
         "callback_data": EmployeeAddFieldCallbackData(field='office').pack()},
        {"text": "Сохранить", "callback_data": EmployeeSaveCallbackData().pack()},
        {"text": "Назад", "callback_data": EmployeeCrudMenuCallbackData().pack()}
    ]
    schema = [1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def employee_add_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": EmployeeAddCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def employee_remove_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": EmployeeCrudMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def employee_office_list_keyboard(offices, status) -> InlineKeyboardMarkup:
    if status == 'add':
        callback_data = EmployeeAddOfficeCallbackData
        back_to = EmployeeAddCallbackData
    else:
        callback_data = EmployeeEditOfficeCallbackData
        back_to = EmployeeEditCallbackData
    actions = []
    for office in offices:
        actions.append({"text": office['title'], "callback_data": callback_data(office=office['id']).pack()})
    actions += [
        {"text": "Назад", "callback_data": back_to(field='office').pack()}
    ]
    schema = [1] * (len(offices) + 1)
    return InlineConstructor.create_kb(actions, schema)


def employee_back_to_keyboard(back_to) -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": back_to().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)

