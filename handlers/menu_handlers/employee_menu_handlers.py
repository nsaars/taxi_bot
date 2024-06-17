from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from functions.cart_crud import get_cart_by_driver_id, get_carts_by_office_id
from functions.driver_crud import get_drivers_by_carts
from functions.employee_crud import get_employee_by_telegram_id
from functions.employee_menu import give_gift, remove_gift
from keyboards.default.employee_menu_default_keyboards import *
from keyboards.inline.employee_menu_keyboards import driver_list_keyboard, cart_product_list_keyboard

texts = {
    "select_driver": "Выберите водителя",
    "choose_driver_gift": "Выберите подарок из корзины водителя.",
    "driver_gift_selection": "✔ Вы выбрали водителя {first_name} и подарок {title} из его корзины.\n\nЕсли пользователь хочет забрать подарок за деньги, возьмите у него\n{quantity}шт * {price} сум = {total_price} сум.",
    "choose_action": "Выберите действие",
    "not_enough_points": "⛔ У водителя отрицательный баланс очков.\nВы можете выдать ему подарок за деньги или предложить водителю убрать из корзины некоторые подарки, чтоб баланс стал положительным.\n\nЕсли пользователь хочет забрать подарок за деньги, возьмите у него\n{quantity}шт * {price} сум = {total_price} сум.",
    "gift_for_money_confirmation": "✅ Вы выдали подарок за деньги. Пользователю вернулись замороженные очки.\nПользователь должен вам {total_price} сум.",
    "gift_for_scores_confirmation": "✅ Вы выдали подарок за очки.",
    "gift_was_not_given": "Подарок не был выдан",
    "remove_gift_confirmation": "❗✅ Вы удалили подарок из корзины пользователя.",
    "no_drivers": "🤔 Ни один водитель не бронировал подарки из вашего офиса."
}


async def employee_menu_handler(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        text = message.text
        if text == TEXT_SELECT_DRIVER:
            current_user, current_employee = get_employee_by_telegram_id(message.chat.id)
            carts = get_carts_by_office_id(current_employee['office_id'])
            drivers = get_drivers_by_carts(carts)
            await state.update_data({'drivers': drivers})
            if not drivers:
                await message.answer(texts["no_drivers"], reply_markup=driver_list_keyboard(drivers))
                return
            await message.answer(texts["select_driver"], reply_markup=driver_list_keyboard(drivers))
            return


async def employee_menu_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await employee_menu_handler(callback_query.message, state)


async def employee_driver_list_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    current_user, current_employee = get_employee_by_telegram_id(callback_query.message.chat.id)

    carts = get_carts_by_office_id(current_employee['office_id'])
    drivers = get_drivers_by_carts(carts)
    await state.update_data({'drivers': drivers})
    await callback_query.message.delete()
    await callback_query.message.answer(texts["select_driver"], reply_markup=driver_list_keyboard(drivers))


async def choose_driver_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    drivers = data.get('drivers')
    current_user, current_employee = get_employee_by_telegram_id(callback_query.message.chat.id)
    chosen_driver = next(driver for driver in drivers if driver['id'] == callback_data.driver)

    chosen_driver_cart = get_cart_by_driver_id(chosen_driver['id'])
    relevant_cart_products = [cart_product for cart_product in chosen_driver_cart['cart_products'] if
                              cart_product['office_id'] == current_employee['office_id']]
    await state.update_data({'chosen_driver_cart': chosen_driver_cart, 'chosen_driver': chosen_driver})
    await callback_query.message.edit_text(texts["choose_driver_gift"],
                                           reply_markup=cart_product_list_keyboard(relevant_cart_products))


async def give_product_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    cart_products = data.get('chosen_driver_cart')['cart_products']
    chosen_driver = data.get('chosen_driver')

    chosen_cart_product = next(
        cart_product for cart_product in cart_products if cart_product['id'] == callback_data.cart_product)
    await state.update_data({'chosen_cart_product': chosen_cart_product})

    price = chosen_cart_product['product']['money_price']
    quantity = chosen_cart_product['quantity']
    message = await callback_query.message.edit_text(

        texts["driver_gift_selection"].format(first_name=chosen_driver['first_name'],
                                              title=chosen_cart_product['product']['title'],
                                              quantity=quantity,
                                              price=price,
                                              total_price=price * quantity),
        reply_markup=None)
    await state.update_data({'delete_message_id': message.message_id})

    await callback_query.message.answer(texts["choose_action"], reply_markup=get_employee_actions())
    await state.set_state('choose_action')


async def choose_action_handler(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        data = await state.get_data()
        chosen_cart_product = data.get('chosen_cart_product')
        text = message.text
        if text == TEXT_GIFT_FOR_SCORES:
            response = give_gift(chosen_cart_product)
            if not response:
                price = chosen_cart_product['product']['money_price']
                quantity = chosen_cart_product['quantity']
                await message.answer(texts["not_enough_points"].format(
                                              quantity=quantity,
                                              price=price,
                                              total_price=price * quantity))
                return

            await message.answer(texts["gift_for_scores_confirmation"], reply_markup=get_employee_menu())
            await state.set_state('employee_menu')
            return
        if text == TEXT_GIFT_FOR_MONEY:
            give_gift(chosen_cart_product, True)
            await message.answer(texts["gift_for_money_confirmation"].format(
                total_price=chosen_cart_product['quantity'] * chosen_cart_product['product']['money_price']),
                reply_markup=get_employee_menu())
            await state.set_state('employee_menu')
            return
        if text == TEXT_BACK:
            current_user, current_employee = get_employee_by_telegram_id(message.chat.id)
            data = await state.get_data()
            chosen_driver_cart = data.get('chosen_driver_cart')
            relevant_cart_products = [cart_product for cart_product in chosen_driver_cart['cart_products'] if
                                      cart_product['office_id'] == current_employee['office_id']]
            await message.answer(texts["gift_was_not_given"], reply_markup=ReplyKeyboardRemove())
            await message.answer(texts["choose_driver_gift"],
                                 reply_markup=cart_product_list_keyboard(relevant_cart_products))

            return
