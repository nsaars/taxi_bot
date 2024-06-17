from aiogram.filters.callback_data import CallbackData


class EmployeeChooseCallbackData(CallbackData, prefix="employee_choose"):
    pass


class EmployeeCallbackData(CallbackData, prefix="employee"):
    employee: int


class EmployeeCrudMenuCallbackData(CallbackData, prefix="employee_crud_menu"):
    pass


class EmployeeViewCallbackData(CallbackData, prefix="employee_view"):
    pass


class EmployeeEditCallbackData(CallbackData, prefix="employee_edit"):
    pass


class EmployeeEditFieldCallbackData(CallbackData, prefix="employee_edit_field"):
    field: str


class EmployeeAddCallbackData(CallbackData, prefix="employee_add"):
    pass


class EmployeeAddFieldCallbackData(CallbackData, prefix="employee_add_field"):
    field: str


class EmployeeAddOfficeCallbackData(CallbackData, prefix="employee_add_office"):
    office: int


class EmployeeEditOfficeCallbackData(CallbackData, prefix="employee_edit_office"):
    office: int


class EmployeeRemoveCallbackData(CallbackData, prefix="employee_remove"):
    pass


class EmployeeSaveCallbackData(CallbackData, prefix="employee_save"):
    pass
