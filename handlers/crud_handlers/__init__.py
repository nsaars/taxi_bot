from aiogram import Router, F
from aiogram.filters import StateFilter, Command

from callbacks.crud_callbacks.manager_crud_callbacks import *
from callbacks.crud_callbacks.product_crud_callbacks import *
from callbacks.crud_callbacks.settings_callbacks import *
from handlers.crud_handlers.crud_menu_handlers import *
from handlers.crud_handlers.driver_crud_handlers.driver_crud_edit_handlers import *
from handlers.crud_handlers.driver_crud_handlers.driver_crud_menu_handlers import *

from callbacks.crud_callbacks.driver_crud_callbacks import *

from callbacks.crud_callbacks.employee_crud_callbacks import *
from handlers.crud_handlers.employee_crud_handlers import *

from callbacks.crud_callbacks.office_crud_callbacks import *
from handlers.crud_handlers.employee_crud_handlers.employee_crud_add_remove_handlers import *
from handlers.crud_handlers.employee_crud_handlers.employee_crud_edit_handlers import *
from handlers.crud_handlers.employee_crud_handlers.employee_crud_menu_handlers import *
from handlers.crud_handlers.manager_crud_handlers import *
from handlers.crud_handlers.manager_crud_handlers.manager_crud_add_remove_handlers import *
from handlers.crud_handlers.manager_crud_handlers.manager_crud_edit_handlers import *
from handlers.crud_handlers.manager_crud_handlers.manager_crud_menu_handlers import *

# Import your handlers
from handlers.crud_handlers.office_crud_handlers import *
from handlers.crud_handlers.office_crud_handlers.office_crud_add_remove_handlers import *
from handlers.crud_handlers.office_crud_handlers.office_crud_edit_handlers import *
from handlers.crud_handlers.office_crud_handlers.office_crud_menu_handlers import *
from handlers.crud_handlers.product_crud_handlers import *
from handlers.crud_handlers.product_crud_handlers.product_crud_add_remove_handlers import *
from handlers.crud_handlers.product_crud_handlers.product_crud_edit_handlers import *
from handlers.crud_handlers.product_crud_handlers.product_crud_menu_handlers import *
from handlers.crud_handlers.settings_handlers import *


def prepare_router() -> Router:
    """
    Создает и настраивает роутер для обработки сообщений и callback-запросов.

    Returns:
        Router: Настроенный роутер.
    """
    router = Router()
    router.message.filter(F.chat.type == "private")

    # Регистрация хендлеров для сообщений
    router.message.register(crud_menu_handler, Command('crud'), StateFilter('*'))
    router.message.register(driver_menu_handler, StateFilter('driver_username'))
    router.message.register(driver_confirm_edition_handler, StateFilter('edit_field'))

    # Регистрация хендлеров для callback-запросов
    router.callback_query.register(back_to_crud_menu, F.data == "crud_menu")
    router.callback_query.register(driver_choose_handler, DriverChooseCallbackData().filter())
    router.callback_query.register(back_to_driver_menu, DriverCrudMenuCallbackData().filter())
    router.callback_query.register(driver_view_handler, DriverViewCallbackData().filter())
    router.callback_query.register(driver_edit_handler, DriverEditCallbackData().filter())
    router.callback_query.register(driver_edit_field_handler, DriverEditFieldCallbackData.filter())

    # Регистрация хендлеров для сообщений
    router.message.register(employee_user_save_handler, StateFilter('employee_add_username'))

    # Регистрация хендлеров для callback-запросов
    router.callback_query.register(employee_select_menu_handler, EmployeeCallbackData.filter())
    router.callback_query.register(employee_menu_handler, EmployeeCrudMenuCallbackData().filter())
    router.callback_query.register(employee_choose_handler, EmployeeChooseCallbackData().filter())
    router.callback_query.register(employee_view_handler, EmployeeViewCallbackData().filter())
    router.callback_query.register(employee_edit_handler, EmployeeEditCallbackData().filter())
    router.callback_query.register(employee_edit_field_handler, EmployeeEditFieldCallbackData.filter())
    router.callback_query.register(employee_edit_office_save_handler, EmployeeEditOfficeCallbackData.filter())
    router.callback_query.register(employee_add_handler, EmployeeAddCallbackData().filter())
    router.callback_query.register(employee_add_field_handler, EmployeeAddFieldCallbackData.filter())
    router.callback_query.register(employee_office_save_handler, EmployeeAddOfficeCallbackData.filter())
    router.callback_query.register(employee_save_handler, EmployeeSaveCallbackData().filter())
    router.callback_query.register(employee_remove_handler, EmployeeRemoveCallbackData().filter())

    # Регистрация хендлеров для сообщений
    router.message.register(office_edit_address_save_handler, StateFilter('office_edit_address'))
    router.message.register(office_edit_title_save_handler, StateFilter('office_edit_title'))
    router.message.register(office_edit_manager_save_handler, StateFilter('office_edit_manager'))
    router.message.register(office_manager_save_handler, StateFilter('office_add_manager'))
    router.message.register(office_address_save_handler, StateFilter('office_add_address'))
    router.message.register(office_title_save_handler, StateFilter('office_add_title'))
    router.message.register(office_update_product_save_handler, StateFilter('product_choose_quantity'))

    # Регистрация хендлеров для callback-запросов
    router.callback_query.register(office_menu_handler, OfficeMenuCallbackData().filter())
    router.callback_query.register(office_choose_handler, OfficeChooseCallbackData().filter())
    router.callback_query.register(office_select_menu_handler, OfficeCallbackData.filter())
    router.callback_query.register(office_view_handler, OfficeViewCallbackData().filter())
    router.callback_query.register(office_edit_handler, OfficeEditCallbackData().filter())
    router.callback_query.register(office_edit_field_handler, OfficeEditFieldCallbackData.filter())
    router.callback_query.register(office_add_handler, OfficeAddCallbackData().filter())
    router.callback_query.register(office_add_field_handler, OfficeAddFieldCallbackData.filter())
    router.callback_query.register(office_save_handler, OfficeSaveCallbackData().filter())
    router.callback_query.register(office_remove_handler, OfficeRemoveCallbackData().filter())
    router.callback_query.register(office_choose_product_handler, OfficeChooseProductCallbackData.filter())
    router.callback_query.register(office_add_product_handler, OfficeAddProductCallbackData.filter())
    router.callback_query.register(office_remove_product_handler, OfficeRemoveProductCallbackData.filter())
    router.callback_query.register(office_update_product_handler, OfficeUpdateProductCallbackData.filter())

    # Регистрация хендлеров для сообщений
    router.message.register(manager_user_save_handler, StateFilter('manager_add_username'))

    # Регистрация хендлеров для callback-запросов
    router.callback_query.register(manager_select_menu_handler, ManagerCallbackData.filter())
    router.callback_query.register(manager_menu_handler, ManagerMenuCallbackData().filter())
    router.callback_query.register(manager_choose_handler, ManagerChooseCallbackData().filter())
    router.callback_query.register(manager_view_handler, ManagerViewCallbackData().filter())
    router.callback_query.register(manager_edit_handler, ManagerEditCallbackData().filter())
    router.callback_query.register(manager_edit_field_handler, ManagerEditFieldCallbackData.filter())
    router.callback_query.register(manager_edit_offices_handler, ManagerChooseOfficeCallbackData.filter())
    router.callback_query.register(manager_add_office_handler, ManagerAddOfficeCallbackData.filter())
    router.callback_query.register(manager_remove_office_handler, ManagerRemoveOfficeCallbackData.filter())
    router.callback_query.register(manager_add_handler, ManagerAddCallbackData().filter())
    router.callback_query.register(manager_add_field_handler, ManagerAddFieldCallbackData.filter())
    router.callback_query.register(manager_save_handler, ManagerSaveCallbackData().filter())
    router.callback_query.register(manager_remove_handler, ManagerRemoveCallbackData().filter())

    # Регистрация хендлеров для сообщений
    router.message.register(product_edit_title_save_handler, StateFilter('product_edit_title'))
    router.message.register(product_edit_money_price_save_handler, StateFilter('product_edit_money_price'))
    router.message.register(product_edit_score_price_save_handler, StateFilter('product_edit_score_price'))
    router.message.register(product_edit_image_save_handler, StateFilter('product_edit_image'))
    router.message.register(product_edit_description_save_handler, StateFilter('product_edit_description'))
    router.message.register(product_title_save_handler, StateFilter('product_add_title'))
    router.message.register(product_money_price_save_handler, StateFilter('product_add_money_price'))
    router.message.register(product_score_price_save_handler, StateFilter('product_add_score_price'))
    router.message.register(product_image_save_handler, StateFilter('product_add_image'))
    router.message.register(product_description_save_handler, StateFilter('product_add_description'))

    # Регистрация хендлеров для callback-запросов
    router.callback_query.register(product_menu_handler, ProductMenuCallbackData().filter())
    router.callback_query.register(product_choose_handler, ProductChooseCallbackData().filter())
    router.callback_query.register(product_select_menu_handler, ProductCallbackData.filter())
    router.callback_query.register(product_view_handler, ProductViewCallbackData().filter())
    router.callback_query.register(product_edit_handler, ProductEditCallbackData().filter())
    router.callback_query.register(product_edit_field_handler, ProductEditFieldCallbackData.filter())
    router.callback_query.register(product_add_handler, ProductAddCallbackData().filter())
    router.callback_query.register(product_add_field_handler, ProductAddFieldCallbackData.filter())
    router.callback_query.register(product_save_handler, ProductSaveCallbackData().filter())
    router.callback_query.register(product_remove_handler, ProductRemoveCallbackData().filter())

    # Регистрация хендлеров для callback-запросов
    router.callback_query.register(settings_menu_handler, SettingsMenuCallbackData().filter())
    router.callback_query.register(settings_update_handler, SettingsUpdateCallbackData.filter())
    return router
