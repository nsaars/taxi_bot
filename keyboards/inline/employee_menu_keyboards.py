from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup

from callbacks.employee_callbacks import DriverCallbackData, GiveCartProductCallbackData, EmployeeMenuCallbackData, \
    EmployeeDriverListCallbackData
from keyboards.inline.consts import InlineConstructor


def driver_list_keyboard(drivers: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    actions = []
    for driver in drivers:
        actions.append({"text": driver['first_name'], "callback_data": DriverCallbackData(driver=driver['id']).pack()})

    actions.append({"text": "Назад", "callback_data": EmployeeMenuCallbackData().pack()})
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)


def cart_product_list_keyboard(cart_products) -> InlineKeyboardMarkup:
    actions = []
    for cart_product in cart_products:
        actions.append({"text": cart_product['product']['title'], "callback_data": GiveCartProductCallbackData(cart_product=cart_product['id']).pack()})

    actions.append({"text": "Назад", "callback_data": EmployeeDriverListCallbackData().pack()})
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)