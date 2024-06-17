from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.employee_crud import get_all_employees
from functions.office_crud import get_office_by_id
from handlers.crud_handlers.helpers import update_message, answer_resend
from keyboards.inline.crud_keyboards.employee_crud_keyboards import (
    employee_menu_keyboard,
    employee_view_keyboard,
    employee_choose_keyboard,
    employee_select_menu_keyboard
)
from handlers.crud_handlers.employee_crud_handlers.employee_crud_config import texts, answer_texts


async def employee_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await update_message(callback_query.message, texts['employee_menu'], employee_menu_keyboard())
    await state.update_data({'message_id': callback_query.message.message_id})


async def employee_choose_handler(callback_query: CallbackQuery, state: FSMContext):

    employees_users = get_all_employees()
    await callback_query.message.edit_text(
        text=texts['employee_choose'],
        reply_markup=employee_choose_keyboard(employees_users)
    )
    await state.update_data({'employees_users': employees_users, 'message_id': callback_query.message.message_id})


async def employee_select_menu_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):

    data = await state.get_data()
    message_id = data.get('message_id')
    employees_users = data.get('employees_users')

    chosen_employee_user = [employee_user for employee_user in employees_users if employee_user['employee']['id'] == callback_data.employee][0]
    office = get_office_by_id(chosen_employee_user['employee']['office_id'])

    answer_text = answer_texts['employee_select'].format(username=chosen_employee_user['user']['telegram_username'])
    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['employee_select_menu'],
                              employee_select_menu_keyboard())
    await state.update_data({'office': office, 'employee': chosen_employee_user['employee'], 'user': chosen_employee_user['user'], 'message_id': msg})


async def employee_view_handler(callback_query: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user = data['user']
    office = data['office']

    text = texts['employee_view'].format(
        id=user['id'],
        username=user['telegram_username'],
        name=user['telegram_name'],
        office=office['title']
    )

    await update_message(callback_query.message, text, employee_view_keyboard())