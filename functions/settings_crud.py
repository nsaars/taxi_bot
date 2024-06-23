from typing import Dict, Any

from requests import HTTPError

from functions.api import api_client


def get_settings():
    try:
        settings_response = api_client.get_items('settings')
        return settings_response['settings'][0]
    except (HTTPError, KeyError, IndexError):
        return


def update_settings(update_data: Dict[str, Any]) -> Dict[str, Any]:
    settings = get_settings()
    return api_client.patch_item('settings', settings['id'], update_data)
