from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.manager_crud import get_all_managers
from functions.office_crud import get_offices_by_manager_id
from handlers.crud_handlers.helpers import update_message, answer_resend
from handlers.crud_handlers.manager_crud_handlers.manager_crud_config import texts, answer_texts
from keyboards.inline.crud_keyboards.manager_crud_keyboards import (
    manager_menu_keyboard,
    manager_view_keyboard,
    manager_choose_keyboard,
    manager_select_menu_keyboard
)


async def manager_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await update_message(callback_query.message, texts['manager_menu'], manager_menu_keyboard())
    await state.update_data({'message_id': callback_query.message.message_id})


async def manager_choose_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для выбора менеджера по имени.
    """
    managers_users = get_all_managers()
    await callback_query.message.edit_text(
        text=texts['manager_choose'],
        reply_markup=manager_choose_keyboard(managers_users)
    )
    await state.update_data({'managers_users': managers_users, 'message_id': callback_query.message.message_id})


async def manager_select_menu_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    managers_users = data.get('managers_users')

    chosen_manager_user = \
        [manager_user for manager_user in managers_users if manager_user['manager']['id'] == callback_data.manager][0]

    answer_text = answer_texts['manager_select'].format(username=chosen_manager_user['user']['telegram_username'])
    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['manager_select_menu'],
                              manager_select_menu_keyboard())
    await state.update_data(
        {'manager': chosen_manager_user['manager'], 'user': chosen_manager_user['user'],
         'message_id': msg})


async def manager_view_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Handler for viewing manager information.
    """
    data = await state.get_data()
    user = data['user']
    manager = data['manager']
    offices = get_offices_by_manager_id(manager['id'])
    offices_string = "у управляющего ещё нет офисов"
    if offices:
        offices_string = '\n'.join([f"{office['title']}" for office in offices])
    text = texts['manager_view'].format(
        id=user['id'],
        username=user['telegram_username'],
        name=user['telegram_name'],
        offices=offices_string
    )

    await update_message(callback_query.message, text, manager_view_keyboard())


