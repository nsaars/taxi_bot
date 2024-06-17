from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callbacks.crud_callbacks.employee_crud_callbacks import EmployeeAddCallbackData
from functions.employee_crud import save_employee, remove_employee, \
    get_employee_by_user_id
from functions.office_crud import get_all_offices
from functions.user_crud import get_user_by_username
from handlers.crud_handlers.employee_crud_handlers.employee_crud_config import texts, answer_texts
from handlers.crud_handlers.helpers import update_message, answer_resend
from keyboards.inline.crud_keyboards.employee_crud_keyboards import (
    employee_menu_keyboard,
    employee_add_keyboard,
    employee_office_list_keyboard,
    employee_back_to_keyboard
)


async def employee_add_handler(callback_query: CallbackQuery, state: FSMContext):
    await update_message(callback_query.message, texts['employee_add'], employee_add_keyboard())


async def employee_add_field_save_handler(message: Message, state: FSMContext, new_employee: dict, answer_text: str,
                                          text: str):
    message_id = (await state.get_data()).get('message_id')

    await state.update_data({'new_employee': new_employee})

    user = new_employee.get('user')
    office = new_employee.get('office')

    msg = await answer_resend(message, message_id, answer_text, text, employee_add_keyboard(user, office))
    await state.update_data({'message_id': msg})


async def employee_add_field_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    if callback_data.field == 'office':
        offices = get_all_offices()
        text = texts['employee_add_office']
        await update_message(callback_query.message, text, employee_office_list_keyboard(offices, 'add'))
        await state.update_data(
            {'field': 'office', 'offices': offices, 'message_id': callback_query.message.message_id})

    elif callback_data.field == 'user':
        text = texts['employee_add_username']
        await state.set_state('employee_add_username')
        await update_message(callback_query.message, text, employee_back_to_keyboard(EmployeeAddCallbackData))
        await state.update_data({'message_id': callback_query.message.message_id})


async def employee_office_save_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_employee = data.get('new_employee')

    offices = data['offices']
    chosen_office = next(office for office in offices if office['id'] == callback_data.office)

    if new_employee:
        new_employee['office'] = chosen_office
    else:
        new_employee = {'office': chosen_office}

    answer_text = answer_texts['employee_add_office'].format(title=chosen_office['title'])
    text = texts['employee_add']

    await employee_add_field_save_handler(callback_query.message, state, new_employee, answer_text, text)


async def employee_user_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_employee = data.get('new_employee')
    username = message.text.replace('@', '')
    user = get_user_by_username(username)

    if not user:
        answer_text = texts['employee_correct_username'].format(username=username)
        text = texts['employee_add_username']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  employee_back_to_keyboard(EmployeeAddCallbackData))
        await state.update_data({'message_id': msg})
        return
    if get_employee_by_user_id(user['id']):
        answer_text = texts['employee_already_exist'].format(username=username)
        text = texts['employee_add_username']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  employee_back_to_keyboard(EmployeeAddCallbackData))
        await state.update_data({'message_id': msg})
        return
    if new_employee:
        new_employee['user'] = user
    else:
        new_employee = {'user': user}

    answer_text = answer_texts['employee_add_user'].format(username=user['telegram_username'])
    text = texts['employee_add']

    await employee_add_field_save_handler(message, state, new_employee, answer_text, text)


async def employee_save_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_employee: dict = data.get('new_employee')
    message_id = data['message_id']

    if new_employee:
        user = new_employee.get('user')
        office = new_employee.get('office')
        if user and office:
            save_employee({'user_id': user['id'], 'office_id': office['id']})

            answer_text = texts['employee_save'].format(office=new_employee['office']['title'])
            msg = await answer_resend(callback_query.message, message_id, answer_text, texts['employee_menu'],
                                      employee_menu_keyboard())
            await state.update_data({'message_id': msg})
            return

    answer_text = texts['employee_fill_fields']
    text = texts['employee_add']

    msg = await answer_resend(callback_query.message, message_id, answer_text, text, employee_add_keyboard())
    await state.update_data({'message_id': msg})


async def employee_remove_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    employee = data['employee']
    message_id = data['message_id']

    remove_employee(employee['id'])

    answer_text = texts['employee_remove']

    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['employee_menu'],
                              employee_menu_keyboard())
    await state.update_data({'message_id': msg})
