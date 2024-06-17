from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from functions.driver_crud import update_driver
from handlers.crud_handlers.driver_crud_handlers.driver_crud_config import texts
from keyboards.inline.crud_keyboards.driver_crud_keyboards import (
    driver_edit_keyboard,
    driver_edit_field_keyboard,
)


async def driver_edit_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    driver = data.get('driver')
    if driver:
        await callback_query.message.edit_text(
            text=texts['driver_edit'],
            reply_markup=driver_edit_keyboard(driver['is_blocked'], driver['trusted'])
        )


async def driver_edit_field_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    driver = data.get('driver')

    if driver:
        if callback_data.field == 'scores':
            await edit_driver_scores(callback_query, state, driver)
        elif callback_data.field == 'is_blocked':
            await confirm_driver_block(callback_query, state, driver)
        elif callback_data.field == 'trusted':
            await toggle_driver_trust(callback_query, state, driver)


async def edit_driver_scores(callback_query: CallbackQuery, state: FSMContext, driver: dict):
    text = texts['driver_scores'].format(scores=driver['scores'])
    await callback_query.message.edit_text(text=text, reply_markup=driver_edit_field_keyboard())
    await state.set_state('edit_field')
    await state.update_data({'field': 'scores', 'message_id': callback_query.message.message_id})


async def confirm_driver_block(callback_query: CallbackQuery, state: FSMContext, driver: dict):
    action = 'разблокировать' if driver['is_blocked'] else 'заблокировать'
    text = texts['confirm_block'].format(action=action)
    await callback_query.message.edit_text(text=text, reply_markup=driver_edit_field_keyboard())
    await state.set_state('edit_field')
    await state.update_data({'field': 'is_blocked', 'message_id': callback_query.message.message_id})


async def toggle_driver_trust(callback_query: CallbackQuery, state: FSMContext, driver: dict):
    update_driver(driver['id'], {'trusted': not driver['trusted']})
    driver['trusted'] = not driver['trusted']
    await state.update_data({'driver': driver})
    await state.set_state(None)
    await callback_query.message.delete()
    not_ = '' if driver['trusted'] else 'не '
    text = texts['update_trust'].format(not_=not_)
    await callback_query.message.answer(text)
    await callback_query.message.answer(
        text=texts['driver_edit'],
        reply_markup=driver_edit_keyboard(driver['is_blocked'], driver['trusted'])
    )


async def driver_confirm_edition_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    bot = message.bot
    driver = data.get('driver')
    field = data.get('field')
    message_id = data.get('message_id')

    if driver and field:
        if field == 'scores':
            await confirm_driver_scores(message, state, driver, message_id)
        elif field == 'is_blocked':
            await confirm_driver_block_action(message, state, driver, message_id)


async def confirm_driver_scores(message: Message, state: FSMContext, driver: dict, message_id: int):
    bot = message.bot
    try:
        scores = float(message.text)
        update_driver(driver['id'], {'scores': scores})
        driver['scores'] = scores
    except ValueError:
        await handle_invalid_scores_input(message, state, message_id)
    else:
        await finalize_scores_update(message, state, driver, scores, message_id)


async def handle_invalid_scores_input(message: Message, state: FSMContext, message_id: int):
    bot = message.bot
    await bot.delete_message(message.chat.id, message_id)
    msg = await message.answer(texts['number_only'], reply_markup=driver_edit_field_keyboard())
    await state.update_data({'message_id': msg.message_id})


async def finalize_scores_update(message: Message, state: FSMContext, driver: dict, scores: float, message_id: int):
    bot = message.bot
    await state.update_data({'driver': driver})
    await state.set_state(None)
    await bot.delete_message(message.chat.id, message_id)
    text = texts['scores_updated'].format(scores=scores)
    await message.answer(text)
    await message.answer(
        text=texts['driver_edit'],
        reply_markup=driver_edit_keyboard(driver['is_blocked'], driver['trusted'])
    )


async def confirm_driver_block_action(message: Message, state: FSMContext, driver: dict, message_id: int):
    bot = message.bot
    if message.text.lower() == "да":
        update_driver(driver['id'], {'is_blocked': not driver['is_blocked']})
        driver['is_blocked'] = not driver['is_blocked']
        await state.update_data({'driver': driver})
        await state.set_state(None)
        await bot.delete_message(message.chat.id, message_id)
        action = 'заблокирован' if driver['is_blocked'] else 'разблокирован'
        text = texts['block_success'].format(action=action)
        await message.answer(text)
        await message.answer(
            text=texts['driver_edit'],
            reply_markup=driver_edit_keyboard(driver['is_blocked'], driver['trusted'])
        )
    else:
        await bot.delete_message(message.chat.id, message_id)
        await message.answer(texts['action_cancelled'])
        await message.answer(
            text=texts['driver_edit'],
            reply_markup=driver_edit_keyboard(driver['is_blocked'], driver['trusted'])
        )
