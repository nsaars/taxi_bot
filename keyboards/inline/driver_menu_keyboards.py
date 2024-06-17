from typing import List, Dict, Any

from aiogram.types import InlineKeyboardMarkup

from callbacks.driver_callbacks import *
from keyboards.inline.consts import InlineConstructor


def choose_product_keyboard(product_index: int, size=None) -> InlineKeyboardMarkup:
    actions = [{"text": "Добавить в корзину", "callback_data": CartAddProductCallbackData(product_index=product_index).pack()}]

    prev_next = 0
    if product_index > 0:
        actions.append(
            {"text": "⬅", "callback_data": CartChooseProductCallbackData(product_index=product_index - 1).pack()})
        prev_next += 1
    if size > product_index + 1:
        actions.append(
            {"text": "➡", "callback_data": CartChooseProductCallbackData(product_index=product_index + 1).pack()})
        prev_next += 1

    actions += [
        {"text": "Назад", "callback_data": DriverMenuCallbackData().pack()}]

    schema = [1, prev_next, 1]
    return InlineConstructor.create_kb(actions, schema)


def product_choose_office_keyboard(offices: List[Dict[str, Any]], product_index: int) -> InlineKeyboardMarkup:
    actions = []
    for office in offices:
        actions.append(
            {"text": office['title'], "callback_data": ProductChooseOfficeCallbackData(office=office['id']).pack()})

    actions.append(
        {"text": "Назад", "callback_data": CartChooseProductCallbackData(product_index=product_index).pack()})
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)


def cart_products_keyboard(cart_products) -> InlineKeyboardMarkup:
    actions = []
    for cart_product in cart_products:
        actions.append({"text": f"{cart_product['product']['title']} - {cart_product['quantity']} шт",
                        "callback_data": CartProductCallbackData(cart_product=cart_product['id']).pack()})

    actions.append({"text": "Назад", "callback_data": DriverMenuCallbackData().pack()})
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)


def cart_product_keyboard(cart_product_id: int) -> InlineKeyboardMarkup:
    actions = [{"text": "🗑️ Удалить из корзины",
                "callback_data": CartProductRemoveCallbackData(cart_product=cart_product_id).pack()},
               {"text": "📝 Изменить количество",
                "callback_data": CartProductUpdateQuantityCallbackData(cart_product=cart_product_id).pack()},
               {"text": "📍 Изменить офис",
                "callback_data": CartProductUpdateOfficeCallbackData(cart_product=cart_product_id).pack()},
               {"text": "Назад", "callback_data": CartCallbackData()}]
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)


def product_update_office_keyboard(offices: List[Dict[str, str]], cart_product_id: int) -> InlineKeyboardMarkup:
    actions = []
    for office in offices:
        actions.append(
            {"text": office['title'], "callback_data": ProductUpdateOfficeCallbackData(office=office['id']).pack()})

    actions.append({"text": "Назад", "callback_data": CartProductCallbackData(cart_product=cart_product_id).pack()})
    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)


def back_keyboard(back: CallbackData) -> InlineKeyboardMarkup:
    actions = [{"text": "Назад", "callback_data": back.pack()}]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)
