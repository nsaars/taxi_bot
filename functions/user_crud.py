from requests.exceptions import HTTPError
from typing import Optional, Dict, Any
from functions.api import api_client


def get_all_users():
    try:
        user_response = api_client.get_items('users')
        return user_response['users']
    except (HTTPError, KeyError, IndexError):
        return []


def create_user(data) -> Dict[str, Any]:
    return api_client.create_item('users', data)


def update_user(user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.patch_item('users', user_id, update_data)


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    try:
        user_response = api_client.get_items('users', {'telegram_username': username})
        return user_response['users'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_user_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
    try:
        user_response = api_client.get_items('users', {'telegram_id': telegram_id})
        return user_response['users'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    try:
        user_response = api_client.get_items('users', {'id': user_id})
        return user_response['users'][0]
    except (HTTPError, KeyError, IndexError):
        return


def remove_user(user_id: int) -> Dict[str, Any]:
    return api_client.delete_items('users', {'id': user_id})
