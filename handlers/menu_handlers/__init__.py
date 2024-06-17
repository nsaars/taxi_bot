from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter

from callbacks.driver_callbacks import *
from callbacks.employee_callbacks import *
from handlers.menu_handlers.driver_menu_handlers.driver_menu_handlers import *
from .driver_menu_handlers.add_product_handlers import *
from .driver_menu_handlers.product_quantity_handler import updated_quantity_save_handler
from .driver_menu_handlers.update_cart_product_handlers import *

from .employee_menu_handlers import *
from .start_handlers import start_handler, get_number_handler


# Import your handlers


def prepare_router() -> Router:
    """
    Создает и настраивает роутер для обработки сообщений и callback-запросов.

    Returns:
        Router: Настроенный роутер.
    """
    router = Router()
    router.message.filter(F.chat.type == "private")

    # Регистрация хендлеров для сообщений
    router.callback_query.register(choose_product_handler, CartChooseProductCallbackData.filter())
    router.callback_query.register(add_product_handler, CartAddProductCallbackData.filter())
    router.callback_query.register(add_product_office_handler, ProductChooseOfficeCallbackData.filter())
    router.callback_query.register(get_cart_product_handler, CartProductCallbackData.filter())
    router.callback_query.register(remove_cart_product_handler, CartProductRemoveCallbackData.filter())
    router.callback_query.register(update_cart_product_quantity_handler, CartProductUpdateQuantityCallbackData.filter())
    router.callback_query.register(update_cart_product_office_handler, CartProductUpdateOfficeCallbackData.filter())
    router.callback_query.register(driver_menu_callback_handler, DriverMenuCallbackData.filter())
    router.callback_query.register(back_to_cart_handler, CartCallbackData.filter())
    router.callback_query.register(update_office_save_handler, ProductUpdateOfficeCallbackData.filter())

    # Registering the message handlers
    router.message.register(start_handler, CommandStart())
    router.message.register(get_number_handler, StateFilter("get_number"))
    router.message.register(driver_menu_handler, StateFilter("driver_menu"))
    router.message.register(add_product_quantity_handler, StateFilter("add_product_quantity"))
    router.message.register(updated_quantity_save_handler, StateFilter("update_quantity_save"))

    # Registering the callback handlers
    router.callback_query.register(employee_menu_callback_handler, EmployeeMenuCallbackData.filter())
    router.callback_query.register(employee_driver_list_callback_handler, EmployeeDriverListCallbackData.filter())
    router.callback_query.register(choose_driver_handler, DriverCallbackData.filter())
    router.callback_query.register(give_product_handler, GiveCartProductCallbackData.filter())

    # Registering the message handlers
    router.message.register(employee_menu_handler, StateFilter("employee_menu"))
    router.message.register(choose_action_handler, StateFilter("choose_action"))

    return router
