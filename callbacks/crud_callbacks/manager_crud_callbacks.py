from aiogram.filters.callback_data import CallbackData


class ManagerChooseCallbackData(CallbackData, prefix="manager_choose"):
    pass


class ManagerCallbackData(CallbackData, prefix="manager_choose"):
    manager: int


class ManagerMenuCallbackData(CallbackData, prefix="manager_menu"):
    pass


class ManagerViewCallbackData(CallbackData, prefix="manager_view"):
    pass


class ManagerEditCallbackData(CallbackData, prefix="manager_edit"):
    pass


class ManagerEditFieldCallbackData(CallbackData, prefix="manager_edit_field"):
    field: str


class ManagerAddCallbackData(CallbackData, prefix="manager_add"):
    pass


class ManagerAddFieldCallbackData(CallbackData, prefix="manager_add_field"):
    field: str


class ManagerChooseOfficeCallbackData(CallbackData, prefix="manager_choose_office"):
    action: str


class ManagerAddOfficeCallbackData(CallbackData, prefix="manager_add_office"):
    office: int


class ManagerRemoveOfficeCallbackData(CallbackData, prefix="manager_remove_office"):
    office: int


class ManagerRemoveCallbackData(CallbackData, prefix="manager_remove"):
    pass


class ManagerSaveCallbackData(CallbackData, prefix="manager_save"):
    pass
