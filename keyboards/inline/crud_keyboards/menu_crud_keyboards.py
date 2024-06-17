from aiogram.types import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from callbacks.crud_callbacks.manager_crud_callbacks import ManagerMenuCallbackData
from callbacks.crud_callbacks.office_crud_callbacks import OfficeMenuCallbackData
from callbacks.crud_callbacks.product_crud_callbacks import ProductMenuCallbackData, ProductChooseCallbackData
from callbacks.crud_callbacks.settings_callbacks import SettingsMenuCallbackData
from keyboards.inline.consts import InlineConstructor
from callbacks.crud_callbacks.driver_crud_callbacks import DriverChooseCallbackData
from callbacks.crud_callbacks.employee_crud_callbacks import EmployeeCrudMenuCallbackData


class OfficeCallbackData(CallbackData, prefix="office"):
    action: str


class ProductCallbackData(CallbackData, prefix="product"):
    action: str


def crud_menu_keyboard(role) -> InlineKeyboardMarkup:
    actions = []

    if role == "admin":
        actions = [
            {"text": "Настройки", "callback_data": SettingsMenuCallbackData().pack()},
            {"text": "Водители", "callback_data": DriverChooseCallbackData().pack()},
            {"text": "Сотрудники", "callback_data": EmployeeCrudMenuCallbackData().pack()},
            {"text": "Управляющие", "callback_data": ManagerMenuCallbackData().pack()}
        ]
    if role == "admin" or role == "manager":
        actions += [
            {"text": "Офисы", "callback_data": OfficeMenuCallbackData().pack()},
            {"text": "Подарки", "callback_data": ProductMenuCallbackData().pack()}
        ]

    schema = [1] * len(actions)
    return InlineConstructor.create_kb(actions, schema)
