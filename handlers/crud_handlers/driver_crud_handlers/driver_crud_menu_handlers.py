from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from functions.driver_crud import get_driver_by_username, get_driver_by_phone_number
from functions.user_crud import get_user_by_id
from handlers.crud_handlers.driver_crud_handlers.driver_crud_config import texts
from handlers.menu_handlers.start_handlers import validate_uzbek_phone_number
from keyboards.inline.crud_keyboards.driver_crud_keyboards import (
    driver_menu_keyboard,
    driver_view_keyboard,
    driver_choose_keyboard,
)


async def driver_choose_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        text=texts['driver_choose'],
        reply_markup=driver_choose_keyboard()
    )
    await state.set_state('driver_username')
    await state.update_data({'message_id': callback_query.message.message_id})


async def driver_menu_handler(message: Message, state: FSMContext):
    bot = message.bot
    data = await state.get_data()
    message_id = data.get('message_id')
    is_correct_phone_number = validate_uzbek_phone_number(message.text)
    if message.text.replace('+', '').isdigit():
        if is_correct_phone_number:
            driver = get_driver_by_phone_number(message.text)
            user = get_user_by_id(driver['user_id'])
        else:
            await bot.delete_message(message.chat.id, message_id)
            msg = await message.answer(
                text=texts['wrong_number'],
                reply_markup=driver_choose_keyboard()
            )
            await state.update_data({'message_id': msg.message_id})
            return
    else:
        driver_username = message.text.replace('@', '')
        user, driver = get_driver_by_username(driver_username)

        if not user:
            await bot.delete_message(message.chat.id, message_id)
            msg = await message.answer(
                text=texts['user_not_registered'],
                reply_markup=driver_choose_keyboard()
            )
            await state.update_data({'message_id': msg.message_id})
            return

    if not driver:
        await bot.delete_message(message.chat.id, message_id)
        msg = await message.answer(
            text=texts['no_driver_with_phone'] if is_correct_phone_number else texts['no_driver_with_username'],
            reply_markup=driver_choose_keyboard()
        )
        await state.update_data({'message_id': msg.message_id})
        return

    await bot.delete_message(message.chat.id, message_id)
    msg = await message.answer(text=texts['select_action'], reply_markup=driver_menu_keyboard())

    await state.set_state(None)
    await state.update_data({'user': user, 'driver': driver, 'message': msg.message_id})


async def back_to_driver_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text=texts['select_action'], reply_markup=driver_menu_keyboard())


async def driver_view_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data['user']
    driver = data['driver']

    text = texts['driver_info'].format(
        first_name=driver['first_name'],
        middle_name=driver['middle_name'] or '',
        last_name=driver['last_name'],
        telegram_id=user['telegram_id'],
        telegram_username=user['telegram_username'],
        telegram_name=user['telegram_name'],
        phone_number=driver['phone_number'],
        yandex_id=driver['yandex_id'],
        callsign=driver['callsign'],
        scores=driver['scores'],
        status='Заблокирован' if driver['is_blocked'] else 'Разблокирован',
        trusted='Да' if driver['trusted'] else 'Нет'
    )

    await callback_query.message.edit_text(text=text, reply_markup=driver_view_keyboard())
