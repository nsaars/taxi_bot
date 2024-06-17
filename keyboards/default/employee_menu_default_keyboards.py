import aiogram

from keyboards.default.consts import DefaultConstructor

TEXT_SELECT_DRIVER = "Выбрать водителя"
TEXT_GIFT_FOR_SCORES = "Выдать подарок за очки"
TEXT_GIFT_FOR_MONEY = "Выдать подарок за деньги"
TEXT_BACK = "Назад"


def get_employee_menu() -> aiogram.types.ReplyKeyboardMarkup:
    actions = [
        {"text": TEXT_SELECT_DRIVER},
    ]
    return DefaultConstructor.create_kb(actions, [1])


def get_employee_actions() -> aiogram.types.ReplyKeyboardMarkup:
    actions = [
        {"text": TEXT_GIFT_FOR_SCORES},
        {"text": TEXT_GIFT_FOR_MONEY},
        {"text": TEXT_BACK}

    ]
    return DefaultConstructor.create_kb(actions, [1, 1, 1])
