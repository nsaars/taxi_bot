from typing import Optional, Dict, Any

from functions.cart_crud import get_cart_by_id, remove_cart_product
from functions.driver_crud import get_driver_by_id, update_driver
from functions.product_office_crud import get_product_office, update_product_office


def give_gift(cart_product, return_scores=False) -> Optional[Dict[str, Any]]:
    cart = get_cart_by_id(cart_product['cart_id'])
    driver = get_driver_by_id(cart['driver_id'])
    if not return_scores and driver['scores'] < 0:
        return None

    product_office = get_product_office(cart_product['product_id'], cart_product['office_id'])
    update_product_office(product_office['id'], {'quantity': product_office['quantity'] - cart_product['quantity']})
    return remove_cart_product(cart_product['id'], change_scores=return_scores)


def remove_gift(cart_product) -> Optional[Dict[str, Any]]:

    return remove_cart_product(cart_product['id'])
