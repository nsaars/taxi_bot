from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.driver_crud import get_driver_by_telegram_id
from functions.product_crud import get_all_products
from functions.product_office_crud import get_products_with_offices
from handlers.menu_handlers.driver_menu_handlers.add_product_handlers import show_product
from handlers.menu_handlers.driver_menu_handlers.driver_menu_config import texts
from handlers.menu_handlers.driver_menu_handlers.helpers import get_or_create_cart
from keyboards.default.driver_menu_default_keyboards import *
from keyboards.inline.driver_menu_keyboards import cart_products_keyboard


async def back_to_cart_handler(callback_query: CallbackQuery):
    current_user, current_driver = get_driver_by_telegram_id(callback_query.message.chat.id)
    current_cart = await get_or_create_cart(current_driver['id'])

    await callback_query.message.delete()
    await callback_query.message.answer(texts["choose_cart_product"],
                                        reply_markup=cart_products_keyboard(current_cart['cart_products']))


async def driver_menu_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    current_user, current_driver = get_driver_by_telegram_id(callback_query.message.chat.id)
    await callback_query.message.delete()
    await callback_query.message.answer(texts["greet_driver"].format(first_name=current_driver['first_name']),
                                        reply_markup=get_driver_menu())
    await state.set_state("driver_menu")


async def driver_menu_handler(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        current_user, current_driver = get_driver_by_telegram_id(message.chat.id)

        text = message.text
        if text == TEXT_SCORE:
            await message.answer(texts["current_scores"].format(scores=current_driver['scores']))
            return

        current_cart = await get_or_create_cart(current_driver['id'])

        if text == TEXT_SELECT_GIFT:
            products = get_products_with_offices()
            if products:
                await message.answer(texts["select_gift"], reply_markup=types.ReplyKeyboardRemove())
                await show_product(message, state, 0, True, products)
                return
            await message.answer(texts["no_gifts"])

        if text == TEXT_CART:
            await message.answer(texts["select_gift"], reply_markup=types.ReplyKeyboardRemove())
            await message.answer(texts["cart_gifts"],
                                 reply_markup=cart_products_keyboard(current_cart['cart_products']))
            return
