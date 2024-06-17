from requests.exceptions import HTTPError
from typing import Optional, Dict, Any, List
from functions.api import api_client
from functions.product_crud import get_all_products


def get_product_office(product_id, office_id) -> Optional[Dict[str, Any]]:
    try:
        office_product_response = api_client.get_items('products_offices',
                                                       {'office_id': office_id, 'product_id': product_id})
        return office_product_response['products_offices'][0]
    except HTTPError:
        return


def update_product_office(product_office_id: int, data: Dict):
    try:
        office_product_response = api_client.patch_item('products_offices', product_office_id, data)
        return office_product_response
    except HTTPError:
        return


def get_products_by_office_id(office_id, not_in=False) -> Optional[List[Dict[str, Any]]]:
    try:
        office_products_response = api_client.get_items('products_offices', {'office_id': office_id})
        office_products_ids = [office_product['product_id'] for office_product in
                               office_products_response['products_offices']]
    except HTTPError:
        office_products_ids = []

    try:
        products_response = api_client.get_items('products')
        products = products_response['products']
        relevant_products = []
        for product in products:
            if not_in and product['id'] not in office_products_ids:
                relevant_products.append(product)
            elif not not_in and product['id'] in office_products_ids:
                relevant_products.append(product)

        return relevant_products
    except HTTPError:
        return []


def get_products_quantity_by_office_id(office_id, not_in=False) -> Optional[List[Dict[Any, Any]]]:
    try:
        office_products_response = api_client.get_items('products_offices', {'office_id': office_id})

        office_products_dict = {office_product['product_id']: office_product['quantity']
                                for office_product in office_products_response['products_offices']}
        products_response = api_client.get_items('products')
        products = products_response['products']
        relevant_products = []
        for product in products:
            if not_in and product['id'] not in list(office_products_dict.keys()):
                relevant_products.append(product)
            elif not not_in and product['id'] in list(office_products_dict.keys()):
                relevant_products.append(product)

        relevant_products = list({'product': product, 'quantity': office_products_dict[product['id']]} for product in
                                 relevant_products)
        return relevant_products
    except HTTPError:
        return []


def office_add_product(product_id: int, office_id: int):
    return api_client.create_item('products_offices',
                                  {'office_id': office_id, 'product_id': product_id, 'quantity': 1})


def office_remove_product(product_id: int, office_id: int, ):
    try:
        office_product_response = api_client.delete_items('products_offices',
                                                          {'product_id': product_id, 'office_id': office_id})

        return office_product_response
    except HTTPError:
        return


def get_office_product_quantity(product_id: int, office_id: int):
    product_office = get_product_office(product_id, office_id)
    return product_office['quantity']


def office_update_product(product_id: int, office_id: int, data: dict):
    try:
        product_office_id = get_product_office(product_id, office_id)['id']
        office_product_response = api_client.patch_item('products_offices', product_office_id, data)

        return office_product_response
    except HTTPError:
        return


def get_offices_by_product_id(product_id) -> Optional[List[Dict[str, Any]]]:
    try:
        office_products_response = api_client.get_items('products_offices', {'product_id': product_id})
        office_ids = [office_product['office_id'] for office_product in
                      office_products_response['products_offices']]
    except HTTPError:
        return []

    try:
        office_response = api_client.get_items('offices')
        offices = office_response['offices']
        relevant_offices = []
        for office in offices:
            if office['id'] in office_ids:
                relevant_offices.append(office)
        return relevant_offices
    except HTTPError:
        return []


def get_offices_unreserved_quantity_by_product_id(product_id) -> Optional[List[Dict[Any, Any]]]:
    try:
        product_offices_response = api_client.get_items('products_offices', {'product_id': product_id})

        product_offices_dict = {
            product_office['office_id']: product_office['quantity'] - product_office['reserved_quantity']
            for product_office in product_offices_response['products_offices']}
        offices_response = api_client.get_items('offices')
        offices = offices_response['offices']
        relevant_offices = []
        for office in offices:
            if office['id'] in product_offices_dict:
                relevant_offices.append({'office': office, 'unreserved_quantity': product_offices_dict[office['id']]})

        return relevant_offices
    except HTTPError:
        return []


def get_products_with_offices():
    try:
        product_offices_response = api_client.get_items('products_offices')
        product_ids = [product_office['product_id'] for product_office in
                       product_offices_response['products_offices']]
    except HTTPError:
        return []

    relevant_products = []
    products = get_all_products()
    for product in products:
        if product['id'] in product_ids:
            relevant_products.append(product)

    return relevant_products
