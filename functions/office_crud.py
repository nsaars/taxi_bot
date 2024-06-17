from requests.exceptions import HTTPError
from typing import Optional, Dict, Any, List
from functions.api import api_client

def get_all_offices() -> Optional[List[Dict[str, Any]]]:
    try:
        offices_response = api_client.get_items('offices')
        return offices_response['offices']
    except (HTTPError, KeyError, IndexError):
        return []


def get_offices_except(office_id) -> Optional[List[Dict[str, Any]]]:
    try:
        offices_response = api_client.get_items('offices', {'id__ne': office_id})
        return offices_response['offices']
    except (HTTPError, KeyError, IndexError):
        return []


def get_offices_by_manager_id(manager_id: int) -> Optional[List[Dict[str, Any]]]:
    try:
        offices_response = api_client.get_items('offices', {'manager_id': manager_id})
        return offices_response['offices']
    except (HTTPError, KeyError, IndexError):
        return []


def get_office_by_id(office_id: int) -> Optional[Dict[str, Any]]:
    try:
        office_response = api_client.get_items('offices', {'id': office_id})
        return office_response['offices'][0]
    except (HTTPError, KeyError, IndexError):
        return


def update_office(office_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.patch_item('offices', office_id, update_data)


def save_office(data) -> Dict[str, Any]:
    return api_client.create_item('offices', data)


def remove_office(office_id: int) -> Dict[str, Any]:
    return api_client.delete_items('offices', {'id': office_id})
