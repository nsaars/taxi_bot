from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.employee_crud import get_employees_by_office_id
from functions.manager_crud import get_manager_by_id
from functions.office_crud import get_all_offices, get_offices_by_manager_id
from functions.product_office_crud import get_products_quantity_by_office_id
from functions.user_crud import get_user_by_id
from handlers.crud_handlers.office_crud_handlers.office_crud_config import texts, answer_texts

from handlers.crud_handlers import answer_resend
from keyboards.inline.crud_keyboards.office_crud_keyboards import (
    office_menu_keyboard,
    office_view_keyboard,
    office_choose_keyboard,
    office_select_menu_keyboard
)


async def office_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        text=texts['office_menu'],
        reply_markup=office_menu_keyboard((await state.get_data()).get('role'))
    )
    await state.update_data({'message_id': callback_query.message.message_id})


async def office_choose_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для выбора офиса по названию.
    """
    data = await state.get_data()
    role = data['role']
    if role == 'manager':
        manager_id = data['manager_id']
        offices = get_offices_by_manager_id(manager_id)
    else:
        offices = get_all_offices()
    await callback_query.message.edit_text(
        text=texts['office_choose'],
        reply_markup=office_choose_keyboard(offices)
    )
    await state.update_data({'offices': offices, 'message_id': callback_query.message.message_id})


async def office_select_menu_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    """
    Обработчик для отображения меню офиса после ввода названия.
    """
    data = await state.get_data()
    message_id = data.get('message_id')
    offices = data.get('offices')

    chosen_office = [office for office in offices if office['id'] == callback_data.office][0]
    manager = get_manager_by_id(chosen_office['manager_id'])
    user = get_user_by_id(manager['user_id'])

    answer_text = answer_texts['office_select'].format(title=chosen_office['title'])
    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['office_select_menu'], office_select_menu_keyboard())
    await state.update_data({'office': chosen_office, 'user': user, 'message_id': msg})


async def office_view_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для просмотра информации об офисе.
    """
    data = await state.get_data()
    office = data['office']
    user = data['user']
    employees_user = get_employees_by_office_id(office['id'])
    products = get_products_quantity_by_office_id(office['id'])
    products_string = "В офисе ещё нет подарков"
    if products:
        products_string = '\n'.join([f"{product['product']['title']} : {product['quantity']} штук" for product in products])
    employees_string = "В офисе ещё нет сотрудников"
    if employees_user:
        employees_string = '\n'.join([f"{employee_user['telegram_username']}" for employee_user in employees_user])
    text = texts['office_view'].format(
        user=user['telegram_username'],
        address=office['address'],
        title=office['title'],
        products=products_string,
        employees=employees_string
    )
    await callback_query.message.edit_text(text=text, reply_markup=office_view_keyboard())
