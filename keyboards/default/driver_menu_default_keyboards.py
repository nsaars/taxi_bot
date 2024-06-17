import aiogram
from keyboards.default.consts import DefaultConstructor

TEXT_SCORE = "❓ Сколько у меня баллов?"
TEXT_SELECT_GIFT = "🎁 Выбрать подарок"
TEXT_CART = "🛒 Корзина"


def get_driver_menu() -> aiogram.types.ReplyKeyboardMarkup:
    actions = [
        {"text": TEXT_SCORE},
        {"text": TEXT_SELECT_GIFT},
        {"text": TEXT_CART}
    ]
    return DefaultConstructor.create_kb(actions, [1, 1, 1])
