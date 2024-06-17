from typing import Optional, Dict, Any, List

from requests.exceptions import HTTPError

from functions.api import api_client
from functions.driver_crud import update_driver, get_driver_by_id
from functions.product_crud import get_all_products, get_product_by_id
from functions.product_office_crud import get_product_office, update_product_office


def create_cart(data) -> Dict[str, Any]:
    cart = api_client.create_item('carts', data)
    cart['cart_products'] = []
    return cart


def get_cart_products_by_id(cart_product_id: int):
    try:
        cart_product_response = api_client.get_items('carts_products', {'id': cart_product_id})
        return cart_product_response['carts_products'][0]
    except (HTTPError, KeyError, IndexError):
        return


def get_cart_product(cart_id, product_id, office_id):
    try:
        cart_product_response = api_client.get_items('carts_products', {'cart_id': cart_id, 'product_id': product_id,
                                                                        'office_id': office_id})
        cart_product = cart_product_response['carts_products'][0]
    except (HTTPError, KeyError, IndexError):
        return

    return cart_product


def cart_product_middleware(cart_product, delta_quantity=None, change_scores=True):
    if not cart_product.get('product'):
        cart_product['product'] = get_product_by_id(cart_product['product_id'])

    product_office = get_product_office(cart_product['product_id'], cart_product['office_id'])
    if delta_quantity is None:
        delta_quantity = cart_product['quantity']
    update_product_office(product_office['id'],
                          {'reserved_quantity': product_office['reserved_quantity'] + delta_quantity})
    if change_scores:
        cart = get_cart_by_id(cart_product['cart_id'])
        driver = get_driver_by_id(cart['driver_id'])
        update_driver(driver['id'],
                      {'scores': driver['scores'] - delta_quantity * cart_product['product']['score_price']})


def create_cart_product(data) -> Dict[str, Any]:
    cart_product = api_client.create_item('carts_products', data)
    cart_product_middleware(cart_product)
    return get_cart_by_id(cart_product['cart_id'])


def update_cart_product(cart_product_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    if 'quantity' in update_data:
        cart_product = get_cart_products_by_id(cart_product_id)
        delta_quantity = update_data['quantity'] - cart_product['quantity']
        print(delta_quantity)
        cart_product_middleware(cart_product, delta_quantity)
    cart_product = api_client.patch_item('carts_products', cart_product_id, update_data)
    return get_cart_by_id(cart_product['cart_id'])


def remove_cart_product(cart_product_id: int, change_scores=True) -> Dict[str, Any]:
    cart_product = get_cart_products_by_id(cart_product_id)
    cart_product_middleware(cart_product, -cart_product['quantity'], change_scores)
    api_client.delete_items('carts_products', {'id': cart_product_id})
    return get_cart_by_id(cart_product['cart_id'])


def get_cart_by_id(cart_id: int):
    try:
        cart_response = api_client.get_items('carts', {'id': cart_id})
        cart = cart_response['carts'][0]
    except (HTTPError, KeyError, IndexError):
        return

    cart['cart_products'] = get_products_by_cart_products_id(get_cart_products_by_cart_id(cart['id']))
    return cart


def get_cart_products_by_cart_id(cart_id: int):
    try:
        cart_product_response = api_client.get_items('carts_products', {'cart_id': cart_id})
        return cart_product_response['carts_products']
    except (HTTPError, KeyError, IndexError):
        return []


def get_products_by_cart_products_id(cart_products):
    products = get_all_products()
    new_cart_products = []
    if products:
        for cart_product in cart_products:
            product = next(product for product in products if cart_product['product_id'] == product['id'])
            cart_product['product'] = product
            new_cart_products.append(cart_product)
    return new_cart_products


def get_cart_products_by_office_id(office_id: int):
    try:
        cart_product_response = api_client.get_items('carts_products', {'office_id': office_id})
        return cart_product_response['carts_products']
    except (HTTPError, KeyError, IndexError):
        return []


def get_cart_products_by_filters(filters: dict):
    try:
        cart_product_response = api_client.get_items('carts_products', filters)
        return cart_product_response['carts_products']
    except (HTTPError, KeyError, IndexError):
        return []


def get_carts_by_office_id(office_id: int) -> List[Optional[Dict[str, Any]]]:
    cart_products = get_cart_products_by_office_id(office_id)
    if not cart_products:
        return []
    return get_carts_by_cart_products(cart_products)


def get_carts_by_cart_products(cart_products: list):
    cart_ids = set(cart_product['cart_id'] for cart_product in cart_products)
    try:
        relevant_carts = []
        cart_response = api_client.get_items('carts')
        carts = cart_response['carts']
        for cart in carts:
            if cart['id'] in cart_ids:
                relevant_carts.append(cart)
        return relevant_carts
    except (HTTPError, KeyError, IndexError):
        return []


def get_cart_by_driver_id(driver_id: int) -> Optional[Dict[str, Any]]:
    try:
        cart_response = api_client.get_items('carts', {'driver_id': driver_id})
        cart = cart_response['carts'][0]
    except (HTTPError, KeyError, IndexError):
        return

    cart['cart_products'] = get_products_by_cart_products_id(get_cart_products_by_cart_id(cart['id']))
    return cart
