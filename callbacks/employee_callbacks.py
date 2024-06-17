from aiogram.filters.callback_data import CallbackData


class DriverCallbackData(CallbackData, prefix="driver"):
    driver: int


class EmployeeMenuCallbackData(CallbackData, prefix="employee_menu"):
    pass


class EmployeeDriverListCallbackData(CallbackData, prefix="employee_driver_list"):
    pass


class GiveCartProductCallbackData(CallbackData, prefix="give_cart_product"):
    cart_product: int
