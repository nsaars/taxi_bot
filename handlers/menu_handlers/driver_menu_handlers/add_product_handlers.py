from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from functions.cart_crud import get_cart_products_by_filters
from functions.driver_crud import get_driver_by_id, get_driver_by_telegram_id
from functions.product_crud import get_all_products
from functions.product_office_crud import get_product_office, \
    get_offices_unreserved_quantity_by_product_id, get_products_with_offices
from functions.settings_crud import get_settings
from handlers.menu_handlers.driver_menu_handlers.driver_menu_config import texts
from handlers.menu_handlers.driver_menu_handlers.product_quantity_handler import product_quantity_handle, update_cart
from keyboards.default import BasicButtons
from keyboards.default.driver_menu_default_keyboards import get_driver_menu
from keyboards.inline.driver_menu_keyboards import choose_product_keyboard, product_choose_office_keyboard


async def show_product(message: types.Message, state: FSMContext, product_index: int, first_message=False, products=None):
    if products is None:
        products = get_products_with_offices()
    product = products[product_index]
    keyboard = choose_product_keyboard(product_index, len(products))

    has_image = 'image' in product and product['image']

    text = texts["product_description"].format(title=product['title'], description=product['description'], score_price=product['score_price'],
                                               money_price=product['money_price'])
    media = InputMediaPhoto(media=product['image'], caption=text) if has_image else None

    if media:
        if message.content_type == 'text' or first_message:
            await message.delete()
            await message.answer_photo(photo=media.media, caption=media.caption, reply_markup=keyboard)
        elif message.content_type == 'photo':
            await message.edit_media(media, reply_markup=keyboard)
    else:
        if message.content_type == 'photo' or first_message:
            await message.delete()
            await message.answer(text=text, reply_markup=keyboard)
        elif message.content_type == 'text':
            await message.edit_text(text, reply_markup=keyboard)


async def choose_product_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    await show_product(callback_query.message, state, callback_data.product_index)


async def add_product_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    current_cart = data.get('current_cart')

    current_user, current_driver = get_driver_by_telegram_id(callback_query.message.chat.id)
    products = get_all_products()
    product_index = callback_data.product_index
    product = products[product_index]

    offices_quantity = get_offices_unreserved_quantity_by_product_id(product['id'])
    offices = []
    for office_quantity in offices_quantity:
        if office_quantity['unreserved_quantity'] > 0:
            offices.append(office_quantity['office'])
    await state.update_data({'offices': offices, 'chosen_product': product, 'chosen_product_index': product_index})

    has_enough_scores = True
    if current_driver['scores'] < product['score_price']:
        if get_cart_products_by_filters(dict(cart_id=current_cart['id'], product_id=product['id'])):
            await callback_query.message.answer(texts["not_enough_scores"])
            await show_product(callback_query.message, state, callback_data.product_index, first_message=True)
            return
        settings = get_settings()
        if not current_driver['trusted'] or not settings['allow_credits']:
            await callback_query.message.answer(texts["not_enough_scores"])
            await show_product(callback_query.message, state, callback_data.product_index, first_message=True)
            return
        await callback_query.message.answer(texts["can_buy_product"])
        has_enough_scores = False
    await state.update_data({'has_enough_scores': has_enough_scores})

    await callback_query.message.delete()
    await callback_query.message.answer(texts["choose_office"],
                                        reply_markup=product_choose_office_keyboard(offices, product_index))


async def add_product_office_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    offices = data.get('offices')
    chosen_office = next(office for office in offices if office['id'] == callback_data.office)
    chosen_product = data.get('chosen_product')
    chosen_product_office = get_product_office(chosen_product['id'], chosen_office['id'])

    await state.update_data({'chosen_office': chosen_office, 'chosen_product_office': chosen_product_office})
    await callback_query.message.delete()
    unreserved_quantity = chosen_product_office['quantity'] - chosen_product_office['reserved_quantity']

    if not data.get('has_enough_scores'):

        await state.set_state('driver_menu')
        await callback_query.message.answer(texts["product_added_to_cart"].format(title=chosen_product['title']),
                                            reply_markup=get_driver_menu())
        await update_cart(callback_query.message, state, data, chosen_office['id'], chosen_product, 1, None)
        return

    await state.set_state('add_product_quantity')
    await callback_query.message.answer(
        texts["enter_quantity"].format(title=chosen_product['title'], unreserved_quantity=unreserved_quantity),
        reply_markup=BasicButtons.back())


async def add_product_quantity_handler(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        data = await state.get_data()
        chosen_office = data.get('chosen_office')
        chosen_product = data.get('chosen_product')
        quantity = await product_quantity_handle(message, state, chosen_office['id'], chosen_product)
        if quantity:
            await state.set_state('driver_menu')
            await message.answer(
                texts["quantity_added_to_cart"].format(quantity=quantity, title=chosen_product['title']),
                reply_markup=get_driver_menu())
