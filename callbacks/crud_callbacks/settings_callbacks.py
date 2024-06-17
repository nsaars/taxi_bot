from typing import Any

from aiogram.filters.callback_data import CallbackData


class SettingsMenuCallbackData(CallbackData, prefix="settings_menu"):
    pass


class SettingsActionCallbackData(CallbackData, prefix="settings_choose_action"):
    action: str


class SettingsUpdateCallbackData(CallbackData, prefix="settings_update_variable"):
    variable: str
    value: Any
