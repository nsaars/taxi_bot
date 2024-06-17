from functions.cart_crud import get_cart_by_driver_id, create_cart, get_cart_product, create_cart_product
from functions.product_crud import get_all_products


async def get_or_create_cart(current_driver_id) -> dict:
    current_cart = get_cart_by_driver_id(current_driver_id)
    if not current_cart:
        current_cart = create_cart({'driver_id': current_driver_id})

    return current_cart


async def get_products(state, data) -> dict:
    products = data.get('products')
    if not products:
        products = get_all_products()
        await state.update_data({'products': products})
    return products
