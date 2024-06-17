from aiogram.filters.callback_data import CallbackData


class ProductCallbackData(CallbackData, prefix="product"):
    product: int


class ProductChooseCallbackData(CallbackData, prefix="product_choose"):
    pass


class ProductMenuCallbackData(CallbackData, prefix="product_menu"):
    pass


class ProductViewCallbackData(CallbackData, prefix="product_view"):
    pass


class ProductEditCallbackData(CallbackData, prefix="product_edit"):
    pass


class ProductEditFieldCallbackData(CallbackData, prefix="product_edit_field"):
    field: str


class ProductAddCallbackData(CallbackData, prefix="product_add"):
    pass


class ProductAddFieldCallbackData(CallbackData, prefix="product_add_field"):
    field: str


class ProductAddTitleCallbackData(CallbackData, prefix="product_add_title"):
    pass


class ProductEditTitleCallbackData(CallbackData, prefix="product_edit_title"):
    pass


class ProductAddMoneyPriceCallbackData(CallbackData, prefix="product_add_money_price"):
    pass


class ProductEditMoneyPriceCallbackData(CallbackData, prefix="product_edit_money_price"):
    pass


class ProductAddScorePriceCallbackData(CallbackData, prefix="product_add_score_price"):
    pass


class ProductEditScorePriceCallbackData(CallbackData, prefix="product_edit_score_price"):
    pass


class ProductAddImageCallbackData(CallbackData, prefix="product_add_image"):
    pass


class ProductEditImageCallbackData(CallbackData, prefix="product_edit_image"):
    pass


class ProductAddDescriptionCallbackData(CallbackData, prefix="product_add_description"):
    pass


class ProductEditDescriptionCallbackData(CallbackData, prefix="product_edit_description"):
    pass


class ProductRemoveCallbackData(CallbackData, prefix="product_remove"):
    pass


class ProductSaveCallbackData(CallbackData, prefix="product_save"):
    pass


class ProductAddProductCallbackData(CallbackData, prefix="product_add_product"):
    product: int


class ProductRemoveProductCallbackData(CallbackData, prefix="product_remove_product"):
    product: int


class ProductUpdateProductCallbackData(CallbackData, prefix="product_update_product"):
    product: int


class ProductChooseProductCallbackData(CallbackData, prefix="product_choose_product"):
    action: str
