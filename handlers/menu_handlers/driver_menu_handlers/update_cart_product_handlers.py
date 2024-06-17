from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.cart_crud import update_cart_product, remove_cart_product
from functions.office_crud import get_office_by_id
from functions.product_office_crud import get_offices_by_product_id, get_product_office
from keyboards.default import BasicButtons
from keyboards.default.driver_menu_default_keyboards import get_driver_menu
from keyboards.inline.driver_menu_keyboards import cart_product_keyboard, cart_products_keyboard, \
    product_update_office_keyboard
from handlers.menu_handlers.driver_menu_handlers.driver_menu_config import texts


async def get_cart_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_cart = data.get('current_cart')
    await message.answer(texts["choose_gift"], reply_markup=cart_products_keyboard(current_cart['cart_products']))


async def show_cart_product(message: types.Message, chosen_cart_product: dict):
    product = chosen_cart_product['product']
    office = get_office_by_id(chosen_cart_product['office_id'])
    text = texts["cart_product_description"].format(title=product['title'],
                                                    description=product['description'],
                                                    quantity=chosen_cart_product['quantity'],
                                                    office_title=office['title'],
                                                    office_address=office['address'],
                                                    score_price=product['score_price'],
                                                    money_price=product['money_price'])
    keyboard = cart_product_keyboard(chosen_cart_product['id'])
    if chosen_cart_product['product'].get('image'):
        await message.answer_photo(photo=chosen_cart_product['product']["image"], caption=text, reply_markup=keyboard)
    else:
        await message.answer(text=text, reply_markup=keyboard)


async def get_cart_product_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    current_cart = data.get('current_cart')
    chosen_cart_product = next(cart_product for cart_product in current_cart['cart_products'] if
                               cart_product['id'] == callback_data.cart_product)
    chosen_product_office = get_product_office(chosen_cart_product['product_id'], chosen_cart_product['office_id'])
    await callback_query.message.delete()

    await show_cart_product(callback_query.message, chosen_cart_product)
    await state.update_data(
        {'chosen_cart_product': chosen_cart_product, 'chosen_product_office': chosen_product_office})


async def remove_cart_product_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    current_cart = remove_cart_product(callback_data.cart_product)
    await state.update_data({'current_cart': current_cart})

    await state.set_state('driver_menu')
    await callback_query.message.answer(texts["gift_removed_from_cart"], reply_markup=get_driver_menu())
    await callback_query.message.delete()


async def update_cart_product_quantity_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chosen_cart_product = data.get('chosen_cart_product')
    await callback_query.message.delete()
    await callback_query.message.answer(texts["enter_new_quantity"].format(quantity=chosen_cart_product['quantity']),
                                        reply_markup=BasicButtons.back())
    await state.set_state('update_quantity_save')


async def update_cart_product_office_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                             state: FSMContext):
    data = await state.get_data()
    chosen_cart_product = data.get('chosen_cart_product')
    offices = get_offices_by_product_id(chosen_cart_product['product']['id'])
    await state.update_data({'offices': offices})

    await callback_query.message.delete()
    await callback_query.message.answer(texts["choose_office_for_pickup"],
                                        reply_markup=product_update_office_keyboard(offices,
                                                                                    callback_data.cart_product))


async def update_office_save_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    offices = data.get('offices')
    chosen_cart_product = data.get('chosen_cart_product')
    chosen_office = next(office for office in offices if office['id'] == callback_data.office)

    current_cart = update_cart_product(chosen_cart_product['id'], {'office_id': chosen_office['id']})
    await state.update_data({'current_cart': current_cart})
    await callback_query.message.delete()
    await state.set_state('driver_menu')
    await callback_query.message.answer(
        texts["office_update_confirmation"].format(product_title=chosen_cart_product['product']['title'],
                                                   office_title=chosen_office['title']), reply_markup=get_driver_menu())
