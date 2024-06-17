from requests.exceptions import HTTPError
from typing import Optional, Tuple, Dict, Any, List
from functions.api import api_client
from functions.user_crud import get_user_by_username, get_user_by_id, get_user_by_telegram_id


def get_all_employees() -> List[Dict[str, Any]]:
    try:
        employee_response = api_client.get_items('employees')
        employees = employee_response['employees']
    except (HTTPError, KeyError, IndexError):
        return []

    return [{'user': get_user_by_id(employee['user_id']), 'employee': employee} for employee in employees]


def get_employee_by_username(username: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    user = get_user_by_username(username)
    if not user:
        return None, None

    employee = get_employee_by_user_id(user['id'])

    return user, employee


def get_employee_by_telegram_id(telegram_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    user = get_user_by_telegram_id(telegram_id)
    if not user:
        return None, None

    employee = get_employee_by_user_id(user['id'])

    return user, employee


def get_employee_by_id(employee_id: int) -> Optional[Dict[str, Any]]:
    try:
        employee_response = api_client.get_items('employees', {'id': employee_id})
        return employee_response['employees'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_employee_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    try:
        manager_response = api_client.get_items('employees', {'user_id': user_id})
        return manager_response['employees'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_employees_by_office_id(office_id: int) -> List[Dict[str, Any]]:
    try:
        employee_response = api_client.get_items('employees', {'office_id': office_id})
        employees = employee_response['employees']
    except (HTTPError, KeyError, IndexError):
        return []

    return [get_user_by_id(employee['user_id']) for employee in employees]


def update_employee(employee_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.patch_item('employees', employee_id, update_data)


def save_employee(data) -> Dict[str, Any]:
    return api_client.create_item('employees', data)


def remove_employee(employee_id: int) -> Dict[str, Any]:
    return api_client.delete_items('employees', {'id': employee_id})
