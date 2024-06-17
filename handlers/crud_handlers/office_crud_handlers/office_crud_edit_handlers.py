from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from requests import HTTPError

from callbacks.crud_callbacks.office_crud_callbacks import OfficeEditFieldCallbackData, OfficeAddCallbackData, \
    OfficeEditCallbackData
from functions.manager_crud import get_manager_by_username
from functions.office_crud import update_office
from functions.product_crud import get_product_by_id
from functions.product_office_crud import get_products_by_office_id, office_add_product, office_remove_product, \
    get_office_product_quantity, office_update_product
from keyboards.inline.crud_keyboards.office_crud_keyboards import (
    office_edit_keyboard,
    office_back_to_keyboard, office_product_keyboard, office_product_choose_keyboard
)
from handlers.crud_handlers.office_crud_handlers.office_crud_config import texts, answer_texts

from handlers.crud_handlers import answer_resend


async def office_edit_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для выбора редактируемого поля офиса.
    """
    await callback_query.message.edit_text(text=texts['office_edit'],
                                           reply_markup=office_edit_keyboard((await state.get_data()).get('role')))


async def office_edit_field_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                    state: FSMContext):
    """
    Обработчик для редактирования конкретного поля офиса.
    """
    data = await state.get_data()
    office = data['office']
    user = data['user']

    if callback_data.field == 'manager':
        text = texts['office_edit_manager'].format(username=user['telegram_username'])
        await state.set_state('office_edit_manager')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=office_back_to_keyboard(OfficeEditCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})

    elif callback_data.field == 'address':
        text = texts['office_edit_address'].format(address=office['address'])
        await state.set_state('office_edit_address')
        await callback_query.message.edit_text(text=text, reply_markup=office_back_to_keyboard(OfficeAddCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})

    elif callback_data.field == 'title':
        text = texts['office_edit_title'].format(title=office['title'])
        await state.set_state('office_edit_title')
        await callback_query.message.edit_text(text=text, reply_markup=office_back_to_keyboard(OfficeAddCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})

    elif callback_data.field == 'product':
        text = texts['office_edit_product']
        await callback_query.message.edit_text(text=text, reply_markup=office_product_keyboard())
        await state.update_data({'message_id': callback_query.message.message_id})


async def office_choose_product_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                        state: FSMContext):
    data = await state.get_data()
    office = data['office']

    if callback_data.action == 'add':
        products = get_products_by_office_id(office['id'], not_in=True)
    else:
        products = get_products_by_office_id(office['id'])
    text = texts['office_choose_product']
    await callback_query.message.edit_text(text=text,
                                           reply_markup=office_product_choose_keyboard(products, callback_data.action))


async def office_add_product_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    data = await state.get_data()
    office = data['office']

    office_add_product(callback_data.product, office['id'])

    text = texts['office_add_product']
    await callback_query.message.edit_text(text=text, reply_markup=office_product_keyboard())


async def office_remove_product_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                        state: FSMContext):
    data = await state.get_data()
    office = data['office']

    office_remove_product(callback_data.product, office['id'])

    text = texts['office_remove_product']
    await callback_query.message.edit_text(text=text, reply_markup=office_product_keyboard())


async def office_update_product_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                        state: FSMContext):
    data = await state.get_data()
    office = data['office']

    product = get_product_by_id(callback_data.product)
    product_quantity = get_office_product_quantity(callback_data.product, office['id'])

    text = texts['office_update_product'].format(quantity=product_quantity, title=product['title'])
    await callback_query.message.edit_text(text=text, reply_markup=office_back_to_keyboard(
        OfficeEditFieldCallbackData(field="product")))
    await state.set_state('product_choose_quantity')
    await state.update_data({'product': product})


async def office_update_product_save_handler(message: Message, state: FSMContext):
    bot = message.bot
    data = await state.get_data()
    office = data['office']
    product = data['product']
    message_id = data['message_id']
    try:
        quantity = int(message.text)
        office_update_product(product['id'], office['id'], {'quantity': quantity})
    except (ValueError, HTTPError):
        await bot.delete_message(message.chat.id, message_id)
        msg = await message.answer("Пожалуйста, отправьте только целое число.",
                                   reply_markup=office_back_to_keyboard(OfficeEditFieldCallbackData(field="product")))
        await state.update_data({'message_id': msg.message_id})
    else:
        await state.set_state(None)
        if quantity == 0:
            office_remove_product(product['id'], office['id'])
            text = texts['office_update_product_remove']
        else:
            text = texts['office_update_product_save'].format(quantity=quantity)

        await bot.delete_message(message.chat.id, message_id)
        await message.answer(text)
        await message.answer(text=texts['office_edit'], reply_markup=office_product_keyboard())


async def office_edit_address_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    address = message.text
    office = data['office']

    update_office(office['id'], {'address': address})
    answer_text = answer_texts['office_update_address'].format(address=address)

    msg = await answer_resend(message, message_id, answer_text, texts['office_edit'],
                              office_edit_keyboard(data.get('role')))
    await state.update_data({'message_id': msg})


async def office_edit_title_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    title = message.text
    office = data['office']
    update_office(office['id'], {'title': title})
    answer_text = answer_texts['office_update_title'].format(title=title)

    msg = await answer_resend(message, message_id, answer_text, texts['office_edit'],
                              office_edit_keyboard(data.get('role')))
    await state.update_data({'message_id': msg})


async def office_edit_manager_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    username = message.text.replace('@', '')
    office = data['office']
    user, manager = get_manager_by_username(username)

    if not manager:
        answer_text = answer_texts['office_correct_username'].format(username=username)
        text = texts['office_edit_manager'].format(username=username)
        msg = await answer_resend(message, message_id, answer_text, text,
                                  office_back_to_keyboard(OfficeEditCallbackData()))
        await state.update_data({'message_id': msg})
        return

    update_office(office['id'], {'manager_id': manager['id']})
    answer_text = answer_texts['office_update_manager'].format(username=user['telegram_username'])

    msg = await answer_resend(message, message_id, answer_text, texts['office_edit'],
                              office_edit_keyboard(data.get('role')))
    await state.update_data({'message_id': msg})
