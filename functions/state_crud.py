from typing import Dict, Any

from requests import HTTPError

from functions.api import api_client
from functions.user_crud import get_user_by_telegram_id


def get_state_by_user_telegram_id(telegram_id: int):
    user = get_user_by_telegram_id(telegram_id)
    if not user:
        return
    try:
        driver_response = api_client.get_items('states', {'user_id': user['id']})
        return driver_response['states'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_state_by_user_id(user_id: int):
    try:
        driver_response = api_client.get_items('states', {'user_id': user_id})
        return driver_response['states'][0]
    except (HTTPError, KeyError, IndexError):
        return


def update_state(state_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.patch_item('states', state_id, update_data)


def create_state(data) -> Dict[str, Any]:
    return api_client.create_item('states', data)
