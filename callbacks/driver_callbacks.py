from aiogram.filters.callback_data import CallbackData


class CartChooseProductCallbackData(CallbackData, prefix="cart_choose_product"):
    product_index: int


class CartAddProductCallbackData(CallbackData, prefix="cart_add_product"):
    product_index: int


class ProductChooseOfficeCallbackData(CallbackData, prefix="product_choose_office"):
    office: int


class CartProductCallbackData(CallbackData, prefix="cart_product"):
    cart_product: int


class CartProductRemoveCallbackData(CallbackData, prefix="cart_product_remove"):
    cart_product: int


class CartProductUpdateQuantityCallbackData(CallbackData, prefix="cart_product_update_quantity"):
    cart_product: int


class CartProductUpdateOfficeCallbackData(CallbackData, prefix="cart_product_update_office"):
    cart_product: int


class ProductUpdateOfficeCallbackData(CallbackData, prefix="product_update_office"):
    office: int


class DriverMenuCallbackData(CallbackData, prefix="driver_menu"):
    pass


class CartCallbackData(CallbackData, prefix="cart"):
    pass
