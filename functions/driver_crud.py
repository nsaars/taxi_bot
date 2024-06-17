from typing import Optional, Tuple, Dict, Any, List

from requests.exceptions import HTTPError

from functions.api import api_client
from functions.user_crud import get_user_by_username, get_user_by_telegram_id


def get_all_drivers():
    try:
        driver_response = api_client.get_items('drivers')
        return driver_response['drivers'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_driver_by_username(username: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    user = get_user_by_username(username)
    if not user:
        return None, None

    driver = get_driver_by_user_id(user['id'])

    return user, driver


def get_driver_by_telegram_id(telegram_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    user = get_user_by_telegram_id(telegram_id)
    if not user:
        return None, None

    driver = get_driver_by_user_id(user['id'])

    return user, driver


def get_driver_by_id(driver_id: int) -> Optional[Dict[str, Any]]:
    try:
        driver_response = api_client.get_items('drivers', {'id': driver_id})
        return driver_response['drivers'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_driver_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    try:
        driver_response = api_client.get_items('drivers', {'user_id': user_id})
        return driver_response['drivers'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_driver_by_phone_number(phone_number: str) -> Optional[Dict[str, Any]]:
    try:
        driver_response = api_client.get_items('drivers', {'phone_number': phone_number})
        return driver_response['drivers'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_drivers_by_carts(carts: list) -> List[Optional[Dict[str, Any]]]:

    driver_ids = [cart['driver_id'] for cart in carts]
    try:
        relevant_drivers = []
        driver_response = api_client.get_items('drivers')
        drivers = driver_response['drivers']
        for driver in drivers:
            if driver['id'] in driver_ids:
                relevant_drivers.append(driver)
        return relevant_drivers
    except (HTTPError, KeyError, IndexError):
        return []


def create_driver(data) -> Dict[str, Any]:
    return api_client.create_item('drivers', data)


def update_driver(driver_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    print(update_data)
    return api_client.patch_item('drivers', driver_id, update_data)
