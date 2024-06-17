from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from functions.settings_crud import get_settings, update_settings
from keyboards.inline.crud_keyboards.menu_crud_keyboards import crud_menu_keyboard
from keyboards.inline.crud_keyboards.settings_keyboards import settings_menu_keyboard


async def settings_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    settings = data.get('settings')
    if not settings:
        settings = get_settings()
        await state.update_data({'settings': settings})

    await callback_query.message.edit_text(text="Выберите действие:", reply_markup=settings_menu_keyboard(**settings))


async def settings_update_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):

    data = await state.get_data()
    settings = data.get('settings')
    if callback_data.variable == 'allow_credits':
        allow_credits = bool(int(callback_data.value))
        update_settings({'allow_credits': allow_credits})
        settings['allow_credits'] = allow_credits
        await state.update_data({'settings': settings})

        await callback_query.message.delete()
        text = "Выберите категорию:"
        answer_text = f"Теперь все {'могут' if allow_credits else 'не могут'} бронировать без баллов"
        await callback_query.message.answer(answer_text)
        await callback_query.message.answer(text, reply_markup=crud_menu_keyboard(data.get('role')))
