from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.employee_crud import update_employee
from functions.office_crud import get_offices_except
from handlers.crud_handlers.helpers import update_message, answer_resend
from keyboards.inline.crud_keyboards.employee_crud_keyboards import (
    employee_edit_keyboard,
    employee_office_list_keyboard
)
from handlers.crud_handlers.employee_crud_handlers.employee_crud_config import texts, answer_texts


async def employee_edit_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Handler for selecting the employee field to edit.
    """
    await update_message(callback_query.message, texts['employee_edit'], employee_edit_keyboard())


async def employee_edit_field_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    """
    Handler for editing a specific employee field.
    """
    data = await state.get_data()
    office = data['office']

    if callback_data.field == 'office':
        offices = get_offices_except(office['id'])
        text = texts['employee_edit_office'].format(title=office['title'])
        await update_message(callback_query.message, text, employee_office_list_keyboard(offices, 'edit'))
        await state.update_data(
            {'field': 'office', 'offices': offices, 'message_id': callback_query.message.message_id})


async def employee_edit_office_save_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                            state: FSMContext):
    data = await state.get_data()
    employee = data['employee']
    offices = data['offices']
    message_id = data['message_id']
    chosen_office = next(office for office in offices if office['id'] == callback_data.office)

    update_employee(employee['id'], {'office_id': chosen_office['id']})
    employee['office_id'] = callback_data.office
    answer_text = answer_texts['employee_update_office'].format(title=chosen_office['title'])

    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['employee_edit'],
                              employee_edit_keyboard())
    await state.update_data({'employee': employee, 'office': chosen_office, 'message_id': msg})
