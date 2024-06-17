from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.product_crud import get_all_products
from keyboards.inline.crud_keyboards.product_crud_keyboards import (
    product_menu_keyboard,
    product_choose_keyboard,
    product_select_menu_keyboard,
)
from handlers.crud_handlers.product_crud_handlers.product_crud_config import texts, answer_texts

from handlers.crud_handlers import answer_resend


async def product_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if message_id:
        msg_id = await answer_resend(callback_query.message, message_id, False, texts['product_menu'], product_menu_keyboard())
    else:
        msg = await callback_query.message.edit_text(texts['product_menu'], reply_markup=product_menu_keyboard())
        msg_id = msg.message_id
    await state.update_data({'message_id': msg_id})


async def product_choose_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для выбора продукта по названию.
    """
    products = get_all_products()
    await callback_query.message.edit_text(
        text=texts['product_choose'],
        reply_markup=product_choose_keyboard(products)
    )
    await state.update_data({'products': products, 'message_id': callback_query.message.message_id})


async def product_select_menu_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    """
    Обработчик для отображения меню продукта после ввода названия.
    """
    data = await state.get_data()
    message_id = data.get('message_id')
    products = data.get('products')

    chosen_product = [product for product in products if product['id'] == callback_data.product][0]

    answer_text = answer_texts['product_select'].format(title=chosen_product['title'])
    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['product_select_menu'],
                              product_select_menu_keyboard())
    await state.update_data({'product': chosen_product, 'message_id': msg})


async def product_view_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для просмотра информации о продукте.
    """
    data = await state.get_data()
    message_id = data['message_id']
    product = data['product']
    text = texts['product_view'].format(
        title=product['title'],
        money_price=product['money_price'],
        score_price=product['score_price'],
        description=product['description'],
    )
    await callback_query.bot.delete_message(callback_query.message.chat.id, message_id)
    msg = await callback_query.message.answer_photo(caption=text, photo=product['image'],
                                                    reply_markup=product_select_menu_keyboard())
    """msg = await answer_resend(callback_query.message, message_id, False, texts['product_select_menu'],
                              product_select_menu_keyboard())"""
    await state.update_data({'message_id': msg.message_id})
