from requests.exceptions import HTTPError
from typing import Optional, Dict, Any, List, Tuple
from functions.api import api_client
from functions.user_crud import get_user_by_username, get_user_by_id, get_user_by_telegram_id


def get_all_managers() -> List[Dict[str, Any]]:
    try:
        manager_response = api_client.get_items('managers')
        managers = manager_response['managers']
    except (HTTPError, KeyError, IndexError):
        return []

    return [{'user': get_user_by_id(manager['user_id']), 'manager': manager} for manager in managers]


def get_manager_by_username(username: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    user = get_user_by_username(username)
    if not user:
        return None, None
    try:
        manager_response = api_client.get_items('managers', {'user_id': user['id']})
        manager = manager_response['managers'][0]
    except (HTTPError, KeyError, IndexError):
        return user, None
    return user, manager


def get_manager_by_id(manager_id: int) -> Optional[Dict[str, Any]]:
    try:
        manager_response = api_client.get_items('managers', {'id': manager_id})
        return manager_response['managers'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_manager_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    try:
        manager_response = api_client.get_items('managers', {'user_id': user_id})
        return manager_response['managers'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_manager_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
    user = get_user_by_telegram_id(telegram_id)
    return get_manager_by_user_id(user['id'])


def update_manager(manager_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.patch_item('managers', manager_id, update_data)


def save_manager(data) -> Dict[str, Any]:
    return api_client.create_item('managers', data)


def remove_manager(manager_id: int) -> Dict[str, Any]:
    return api_client.delete_items('managers', {'id': manager_id})
