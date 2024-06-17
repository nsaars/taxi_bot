from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from data.config import ADMIN
from functions.employee_crud import get_employee_by_id, get_employee_by_telegram_id
from functions.manager_crud import get_manager_by_id, get_manager_by_telegram_id
from keyboards.inline.crud_keyboards.menu_crud_keyboards import crud_menu_keyboard


async def crud_menu_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    role = None
    await state.clear()

    if telegram_id == ADMIN:
        role = 'admin'
    else:

        manager = get_manager_by_telegram_id(telegram_id)

        if manager:
            await state.update_data({'manager_id': manager['id']})
            role = 'manager'

    if not role:
        return
    await state.update_data({'role': role})
    await message.answer("Выберите категорию:", reply_markup=crud_menu_keyboard(role))


async def back_to_crud_menu(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    role = data.get('role')
    manager_id = data.get('manager_id')
    await state.clear()
    data = {'role': role}
    if manager_id:
        data['manager_id'] = manager_id
    await state.set_data(data)

    await callback_query.message.edit_text("Выберите категорию:", reply_markup=crud_menu_keyboard(role))
