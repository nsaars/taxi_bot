from aiogram.types import InlineKeyboardMarkup
from callbacks.crud_callbacks.product_crud_callbacks import *
from keyboards.inline.consts import InlineConstructor
from typing import List, Dict, Optional


def product_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Добавить продукт", "callback_data": ProductAddCallbackData().pack()},
        {"text": "Выбрать продукт", "callback_data": ProductChooseCallbackData().pack()},
        {"text": "Назад", "callback_data": "crud_menu"}
    ]
    schema = [1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def product_choose_keyboard(products: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    actions = []
    for product in products:
        actions.append({"text": product['title'], "callback_data": ProductCallbackData(product=product['id']).pack()})

    actions.append({"text": "Назад", "callback_data": ProductMenuCallbackData().pack()})
    schema = [1] * (len(products) + 1)
    return InlineConstructor.create_kb(actions, schema)


def product_select_menu_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Получить информацию о продукте", "callback_data": ProductViewCallbackData().pack()},
        {"text": "Исправить информацию о продукте", "callback_data": ProductEditCallbackData().pack()},
        {"text": "Удалить продукт", "callback_data": ProductRemoveCallbackData().pack()},
        {"text": "Назад", "callback_data": ProductMenuCallbackData().pack()},
    ]
    schema = [1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def product_view_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Исправить информацию о продукте", "callback_data": ProductEditCallbackData().pack()},
        {"text": "Назад", "callback_data": ProductMenuCallbackData().pack()}
    ]
    schema = [1, 1]
    return InlineConstructor.create_kb(actions, schema)


def product_edit_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Название", "callback_data": ProductEditFieldCallbackData(field="title").pack()},
        {"text": "Цена (деньги)", "callback_data": ProductEditFieldCallbackData(field="money_price").pack()},
        {"text": "Цена (очки)", "callback_data": ProductEditFieldCallbackData(field="score_price").pack()},
        {"text": "Изображение", "callback_data": ProductEditFieldCallbackData(field="image").pack()},
        {"text": "Описание", "callback_data": ProductEditFieldCallbackData(field="description").pack()},
        {"text": "Назад", "callback_data": ProductChooseCallbackData().pack()}
    ]
    schema = [1, 1, 1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def product_edit_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": ProductMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def product_add_keyboard(title: Optional[str] = None, money_price: Optional[str] = None, score_price: Optional[str] = None,
                         image: Optional[str] = None, description: Optional[str] = None) -> InlineKeyboardMarkup:
    actions = [
        {"text": f"Название: {title}" if title else "Добавить название",
         "callback_data": ProductAddFieldCallbackData(field='title').pack()},
        {"text": f"Цена (деньги): {money_price}" if money_price else "Добавить цену (деньги)",
         "callback_data": ProductAddFieldCallbackData(field='money_price').pack()},
        {"text": f"Цена (очки): {score_price}" if score_price else "Добавить цену (очки)",
         "callback_data": ProductAddFieldCallbackData(field='score_price').pack()},
        {"text": f"Изображение добавлено" if image else "Добавить изображение",
         "callback_data": ProductAddFieldCallbackData(field='image').pack()},
        {"text": f"Описание добавлено" if description else "Добавить описание",
         "callback_data": ProductAddFieldCallbackData(field='description').pack()},
        {"text": "Сохранить", "callback_data": ProductSaveCallbackData().pack()},
        {"text": "Назад", "callback_data": ProductMenuCallbackData().pack()}
    ]
    schema = [1, 1, 1, 1, 1, 1, 1]
    return InlineConstructor.create_kb(actions, schema)


def product_add_field_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": ProductAddCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def product_remove_keyboard() -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": ProductMenuCallbackData().pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)


def product_back_to_keyboard(back_to: CallbackData) -> InlineKeyboardMarkup:
    actions = [
        {"text": "Назад", "callback_data": back_to.pack()}
    ]
    schema = [1]
    return InlineConstructor.create_kb(actions, schema)
