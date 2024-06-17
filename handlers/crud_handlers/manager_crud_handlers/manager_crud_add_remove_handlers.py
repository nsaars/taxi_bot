from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callbacks.crud_callbacks.manager_crud_callbacks import ManagerAddCallbackData
from functions.manager_crud import save_manager, remove_manager, \
    get_manager_by_user_id
from functions.user_crud import get_user_by_username
from handlers.crud_handlers.helpers import update_message, answer_resend
from handlers.crud_handlers.manager_crud_handlers.manager_crud_config import texts, answer_texts
from keyboards.inline.crud_keyboards.manager_crud_keyboards import (
    manager_menu_keyboard,
    manager_add_keyboard,
    manager_back_to_keyboard
)


async def manager_add_handler(callback_query: CallbackQuery, state: FSMContext):
    await update_message(callback_query.message, texts['manager_add'], manager_add_keyboard())


async def manager_field_save_handler(message: Message, state: FSMContext, new_manager: dict, answer_text: str,
                                     text: str):
    message_id = (await state.get_data()).get('message_id')

    await state.update_data({'new_manager': new_manager})

    user = new_manager.get('user')

    msg = await answer_resend(message, message_id, answer_text, text, manager_add_keyboard(user))
    await state.update_data({'message_id': msg})


async def manager_add_field_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    if callback_data.field == 'user':
        text = texts['manager_add_username']
        await state.set_state('manager_add_username')
        await update_message(callback_query.message, text, manager_back_to_keyboard(ManagerAddCallbackData))
        await state.update_data({'message_id': callback_query.message.message_id})


async def manager_user_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_manager = data.get('new_manager')
    username = message.text.replace('@', '')
    user = get_user_by_username(username)

    if not user:
        answer_text = texts['manager_correct_username'].format(username=username)
        text = texts['manager_add_username']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  manager_back_to_keyboard(ManagerAddCallbackData))
        await state.update_data({'message_id': msg})
        return
    if get_manager_by_user_id(user['id']):
        answer_text = texts['manager_already_exist'].format(username=username)
        text = texts['manager_add_username']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  manager_back_to_keyboard(ManagerAddCallbackData))
        await state.update_data({'message_id': msg})
        return
    if new_manager:
        new_manager['user'] = user
    else:
        new_manager = {'user': user}

    answer_text = answer_texts['manager_add_user'].format(username=user['telegram_username'])
    text = texts['manager_add']

    await manager_field_save_handler(message, state, new_manager, answer_text, text)


async def manager_save_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_manager: dict = data.get('new_manager')
    message_id = data['message_id']

    if new_manager:
        user = new_manager.get('user')
        if user:
            save_manager({'user_id': user['id']})

            answer_text = texts['manager_save']
            msg = await answer_resend(callback_query.message, message_id, answer_text, texts['manager_menu'],
                                      manager_menu_keyboard())
            await state.update_data({'message_id': msg})
            return

    answer_text = texts['manager_fill_fields']
    text = texts['manager_add']

    msg = await answer_resend(callback_query.message, message_id, answer_text, text, manager_add_keyboard())
    await state.update_data({'message_id': msg})


async def manager_remove_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    manager = data['manager']
    message_id = data['message_id']

    remove_manager(manager['id'])

    answer_text = texts['manager_remove']

    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['manager_menu'],
                              manager_menu_keyboard())
    await state.update_data({'message_id': msg})
