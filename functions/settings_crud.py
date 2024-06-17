from typing import Dict, Any

from requests import HTTPError

from functions.api import api_client


def get_settings():
    try:
        cart_product_response = api_client.get_items('settings', {'id': 1})
        return cart_product_response['settings'][0]
    except (HTTPError, KeyError, IndexError):
        return


def update_settings(update_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.patch_item('settings', 1, update_data)
