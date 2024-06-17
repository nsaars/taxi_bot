from aiogram.filters.callback_data import CallbackData


class DriverChooseCallbackData(CallbackData, prefix="driver_choose"):
    pass


class DriverCrudMenuCallbackData(CallbackData, prefix="driver_crud_menu"):
    pass


class DriverViewCallbackData(CallbackData, prefix="driver_view"):
    pass


class DriverEditCallbackData(CallbackData, prefix="driver_edit"):
    pass


class DriverEditFieldCallbackData(CallbackData, prefix="driver_edit_field"):
    field: str
