from requests.exceptions import HTTPError
from typing import Optional, Dict, Any, List
from functions.api import api_client


def get_all_products() -> Optional[List[Dict[str, Any]]]:
    try:
        products_response = api_client.get_items('products')
        return products_response['products']
    except (HTTPError, KeyError, IndexError):
        return []


def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    try:
        product_response = api_client.get_items('products', {'id': product_id})
        return product_response['products'][0]
    except (HTTPError, KeyError, IndexError):
        return


def update_product(product_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.patch_item('products', product_id, update_data)


def save_product(data) -> Dict[str, Any]:
    return api_client.create_item('products', data)


def remove_product(product_id: int) -> Dict[str, Any]:
    return api_client.delete_items('products', {'id': product_id})
