from aiogram.filters.callback_data import CallbackData


class OfficeCallbackData(CallbackData, prefix="office"):
    office: int


class OfficeChooseCallbackData(CallbackData, prefix="office_choose"):
    pass


class OfficeMenuCallbackData(CallbackData, prefix="office_menu"):
    pass


class OfficeViewCallbackData(CallbackData, prefix="office_view"):
    pass


class OfficeEditCallbackData(CallbackData, prefix="office_edit"):
    pass


class OfficeEditFieldCallbackData(CallbackData, prefix="office_edit_field"):
    field: str


class OfficeAddCallbackData(CallbackData, prefix="office_add"):
    pass


class OfficeAddFieldCallbackData(CallbackData, prefix="office_add_field"):
    field: str


class OfficeAddManagerCallbackData(CallbackData, prefix="office_add_manager"):
    pass


class OfficeEditManagerCallbackData(CallbackData, prefix="office_edit_manager"):
    pass


class OfficeAddAddressCallbackData(CallbackData, prefix="office_add_address"):
    pass


class OfficeEditAddressCallbackData(CallbackData, prefix="office_edit_address"):
    pass


class OfficeAddTitleCallbackData(CallbackData, prefix="office_add_title"):
    pass


class OfficeEditTitleCallbackData(CallbackData, prefix="office_edit_title"):
    pass


class OfficeRemoveCallbackData(CallbackData, prefix="office_remove"):
    pass


class OfficeSaveCallbackData(CallbackData, prefix="office_save"):
    pass


class OfficeAddProductCallbackData(CallbackData, prefix="office_add_product"):
    product: int


class OfficeRemoveProductCallbackData(CallbackData, prefix="office_remove_product"):
    product: int


class OfficeUpdateProductCallbackData(CallbackData, prefix="office_update_product"):
    product: int


class OfficeChooseProductCallbackData(CallbackData, prefix="office_choose_product"):
    action: str
