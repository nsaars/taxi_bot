from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callbacks.crud_callbacks.office_crud_callbacks import OfficeAddCallbackData
from functions.manager_crud import get_manager_by_username
from functions.office_crud import save_office, remove_office
from functions.user_crud import get_user_by_id
from keyboards.inline.crud_keyboards.office_crud_keyboards import (
    office_menu_keyboard,
    office_add_keyboard,
    office_back_to_keyboard
)
from handlers.crud_handlers.office_crud_handlers.office_crud_config import texts, answer_texts

from handlers.crud_handlers import answer_resend


async def office_add_handler(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=texts['office_add'], reply_markup=office_add_keyboard())


async def office_add_field_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    if callback_data.field == 'manager':
        text = texts['office_add_manager']
        await state.set_state('office_add_manager')
        await callback_query.message.edit_text(text=text, reply_markup=office_back_to_keyboard(OfficeAddCallbackData()))

    elif callback_data.field == 'address':
        text = texts['office_add_address']
        await state.set_state('office_add_address')
        await callback_query.message.edit_text(text=text, reply_markup=office_back_to_keyboard(OfficeAddCallbackData()))

    elif callback_data.field == 'title':
        text = texts['office_add_title']
        await state.set_state('office_add_title')
        await callback_query.message.edit_text(text=text, reply_markup=office_back_to_keyboard(OfficeAddCallbackData()))


async def office_field_save_handle(message: Message, state: FSMContext, new_office, answer_text, text):
    message_id = (await state.get_data()).get('message_id')

    await state.update_data({'new_office': new_office})

    manager = new_office.get('manager')
    address = new_office.get('address')
    title = new_office.get('title')

    user = None
    if manager:
        user = get_user_by_id(manager['user_id'])

    msg = await answer_resend(message, message_id, answer_text, text,
                              office_add_keyboard(user, address, title))
    await state.update_data({'message_id': msg})


async def office_manager_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_office = data.get('new_office')
    username = message.text.replace('@', '')
    user, manager = get_manager_by_username(username)

    if not manager:
        answer_text = answer_texts['office_correct_username'].format(username=username)
        text = texts['office_add_manager']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  office_back_to_keyboard(OfficeAddCallbackData()))
        await state.update_data({'message_id': msg})
        return

    if new_office:
        new_office['manager'] = manager
    else:
        new_office = {'manager': manager}

    answer_text = answer_texts['office_add_manager'].format(username=user['telegram_username'])
    text = texts['office_add']
    await office_field_save_handle(message, state, new_office, answer_text, text)


async def office_address_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    address = message.text
    new_office = data.get('new_office')

    if new_office:
        new_office['address'] = address
    else:
        new_office = {'address': address}

    answer_text = answer_texts['office_add_address'].format(address=address)
    text = texts['office_add']

    await office_field_save_handle(message, state, new_office, answer_text, text)


async def office_title_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    title = message.text
    new_office = data.get('new_office')

    if new_office:
        new_office['title'] = title
    else:
        new_office = {'title': title}

    answer_text = answer_texts['office_add_title'].format(title=title)
    text = texts['office_add']
    await office_field_save_handle(message, state, new_office, answer_text, text)


async def office_save_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_office: dict = data.get('new_office')
    message_id = data['message_id']

    if new_office:
        manager = new_office.get('manager')
        address = new_office.get('address')
        title = new_office.get('title')
        if manager and address and title:
            save_office({'manager_id': int(manager['id']), 'address': address, 'title': title})

            answer_text = texts['office_save']
            msg = await answer_resend(callback_query.message, message_id, answer_text, texts['office_menu'],
                                      office_menu_keyboard(data.get('role')))
            await state.update_data({'new_office': {}, 'message_id': msg})
            return

        answer_text = texts['office_fill_fields']
        text = texts['office_add']

        await office_field_save_handle(callback_query.message, state, new_office, answer_text, text)


async def office_remove_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    office = data['office']
    message_id = data['message_id']

    remove_office(office['id'])

    answer_text = texts['office_remove']

    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['office_menu'],
                              office_menu_keyboard(data.get('role')))
    await state.update_data({'message_id': msg})
