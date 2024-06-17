from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.office_crud import get_office_by_id, get_offices_by_manager_id, \
    update_office
from handlers.crud_handlers.helpers import update_message, answer_resend
from handlers.crud_handlers.manager_crud_handlers.manager_crud_config import texts, answer_texts
from keyboards.inline.crud_keyboards.manager_crud_keyboards import (
    manager_edit_keyboard,
    manager_office_list_keyboard,
    manager_edit_office_keyboard
)


async def manager_edit_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Handler for selecting the manager field to edit.
    """
    await update_message(callback_query.message, texts['manager_edit'], manager_edit_keyboard())


async def manager_edit_field_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    """
    Handler for editing a specific manager field.
    """
    if callback_data.field == 'office':
        text = texts['manager_edit_office']
        await update_message(callback_query.message, text, manager_edit_office_keyboard())


async def manager_edit_offices_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    manager = data['manager']

    offices = get_offices_by_manager_id(manager['id'])

    text = texts[f'manager_{callback_data.action}_office']
    await update_message(callback_query.message, text, manager_office_list_keyboard(offices, callback_data.action))


async def manager_add_office_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    manager = data['manager']
    message_id = data['message_id']
    office = get_office_by_id(callback_data.office)
    update_office(callback_data.office, {'manager_id': manager['id']})

    answer_text = answer_texts['manager_added_office'].format(title=office['title'])
    text = texts[f'manager_edit_office']
    msg = await answer_resend(callback_query.message, message_id, answer_text, text,
                              manager_edit_keyboard())
    await state.update_data({'message_id': msg})


async def manager_remove_office_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id']
    office = get_office_by_id(callback_data.office)
    update_office(callback_data.office, {'manager_id': None})

    answer_text = answer_texts['manager_removed_office'].format(title=office['title'])
    text = texts[f'manager_edit_office']
    msg = await answer_resend(callback_query.message, message_id, answer_text, text,
                              manager_edit_keyboard())
    await state.update_data({'message_id': msg})
