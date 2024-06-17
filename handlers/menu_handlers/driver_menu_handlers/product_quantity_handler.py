from aiogram import types
from aiogram.fsm.context import FSMContext

from functions.cart_crud import create_cart_product, update_cart_product, \
    remove_cart_product, get_cart_product
from functions.driver_crud import get_driver_by_id, get_driver_by_telegram_id
from functions.settings_crud import get_settings
from handlers.menu_handlers.driver_menu_handlers.driver_menu_config import texts
from handlers.menu_handlers.driver_menu_handlers.update_cart_product_handlers import show_cart_product
from keyboards.default import BasicButtons
from keyboards.default.driver_menu_default_keyboards import get_driver_menu
from keyboards.inline.driver_menu_keyboards import product_choose_office_keyboard


async def updated_quantity_save_handler(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        data = await state.get_data()
        chosen_cart_product = data.get('chosen_cart_product')
        quantity = await product_quantity_handle(message, state, chosen_cart_product['office_id'],
                                                 chosen_cart_product['product'], chosen_cart_product)
        if quantity:
            await state.set_state('driver_menu')
            await message.answer(
                texts["new_quantity"].format(product_title=chosen_cart_product['product']['title'], quantity=quantity),
                reply_markup=get_driver_menu())


async def product_quantity_handle(message: types.Message, state: FSMContext, office_id, product, cart_product=None):
    if message.content_type != 'text':
        return

    data = await state.get_data()
    text = message.text

    if text == '◀️Назад':
        await handle_back_action(message, state, data, cart_product)
        return

    try:
        quantity = int(text)
    except ValueError:
        await message.answer(texts["enter_integer"], reply_markup=BasicButtons.back())
        return

    if quantity == 0:
        await handle_zero_quantity(message, state, cart_product)
        return

    if not await handle_quantity_check(message, state, data, product, quantity, cart_product, office_id):
        return

    return await update_cart(message, state, data, office_id, product, quantity, cart_product)


async def handle_back_action(message, state, data, cart_product):
    await message.answer(texts["quantity_not_changed"], reply_markup=types.ReplyKeyboardRemove())
    if cart_product:
        chosen_cart_product = data.get('chosen_cart_product')
        await show_cart_product(message, chosen_cart_product)
    else:
        offices = data.get('offices')
        product_index = data.get('chosen_product_index')
        await message.answer(texts["choose_office"],
                             reply_markup=product_choose_office_keyboard(offices, product_index))
    await state.set_state(None)


async def handle_zero_quantity(message, state, cart_product):
    if cart_product:
        remove_cart_product(cart_product['id'])
        await state.set_state('driver_menu')
        await message.answer(texts["gift_removed_from_cart"], reply_markup=get_driver_menu())
    else:
        await message.answer(texts["choose_positive_integer"])


async def handle_quantity_check(message, state, data, product, quantity, cart_product, office_id):
    current_user, current_driver = get_driver_by_telegram_id(message.chat.id)
    chosen_product_office = data.get('chosen_product_office')
    current_cart = data.get('current_cart')

    unreserved_quantity = chosen_product_office['quantity'] - chosen_product_office['reserved_quantity']
    cart_product_quantity = 0 if not cart_product else cart_product['quantity']

    if quantity > unreserved_quantity + cart_product_quantity:
        await message.answer(texts["max_quantity"].format(max_quantity=unreserved_quantity + cart_product_quantity),
                             reply_markup=BasicButtons.back())
        return False

    delta_quantity = quantity - cart_product_quantity
    if delta_quantity > 0:
        if current_driver['scores'] < product['score_price'] * delta_quantity:

            settings = get_settings()
            if not settings['allow_credits'] or not current_driver['trusted']:

                if not cart_product and quantity == 1:
                    await message.answer(texts["not_enough_scores"].format(product_title=product['title']))
                    return False

            if quantity > 1:
                if not cart_product and get_cart_product(cart_id=current_cart['id'], product_id=product['id'], office_id=office_id):
                    await message.answer(texts["not_enough_scores"].format(product_title=product['title']))
                    return False
                await message.answer(
                    texts["not_enough_scores_multiple"].format(quantity=quantity, product_title=product['title']))
                return False
    return True


async def update_cart(message, state, data, office_id, product, quantity, cart_product):
    current_cart = data.get('current_cart')
    if not cart_product:
        cart_product = get_cart_product(cart_id=current_cart['id'], product_id=product['id'], office_id=office_id)
        if not cart_product:
            current_cart = create_cart_product(
                {'cart_id': current_cart['id'], 'product_id': product['id'], 'office_id': office_id,
                 'quantity': quantity})

    if cart_product:
        print(quantity)
        current_cart = update_cart_product(cart_product['id'], {'quantity': quantity})

    await state.update_data({'current_cart': current_cart})
    return quantity
