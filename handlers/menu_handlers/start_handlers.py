import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from functions.cart_crud import create_cart, get_cart_by_driver_id
from functions.driver_crud import get_driver_by_user_id, get_driver_by_phone_number, update_driver, create_driver
from functions.employee_crud import get_employee_by_user_id
from functions.user_crud import get_user_by_telegram_id, create_user, get_user_by_id, update_user, remove_user
from keyboards.default.driver_menu_default_keyboards import get_driver_menu
from keyboards.default.start_keyboards import *
from keyboards.default.employee_menu_default_keyboards import get_employee_menu
from utils.number import YandexFleetAPI

yandex_api = YandexFleetAPI()

texts = {
    "greet_driver": "Здравствуйте, {first_name}, у вас {scores} баллов.",
    "select_action": "Выберите действие",
    "greet_user": "Здравствуйте, {user_telegram_name}. Если вы водитель, отправьте номер телефона, указанный в яндексе.",
    "send_phone_or_contact": "Отправьте номер телефона или контакт",
    "request_admin_role": "Попросите администратора добавить вам роль и нажмите /start",
    "invalid_phone_format": "Отправьте номер телефона в формате +998901112233",
    "driver_not_registered": "На этот номер не зарегистрирован водитель."
}


def validate_uzbek_phone_number(phone_number: str) -> bool:
    pattern = r'\+998\s?(90|91|93|94|95|97|98|99)\s?\d{7}'
    return bool(re.match(pattern, phone_number))


async def start_handler(message: types.Message, state: FSMContext):
    user_telegram_name = message.from_user.full_name

    user = get_user_by_telegram_id(message.from_user.id)

    if user is not None:
        update_user(user['id'], {"telegram_username": message.from_user.username, "telegram_name": message.from_user.full_name})
        driver = get_driver_by_user_id(user['id'])
        if driver:
            current_cart = get_cart_by_driver_id(driver['id'])
            if not current_cart:
                current_cart = create_cart({'driver_id': driver['id']})

            await message.answer(texts["greet_driver"].format(first_name=driver['first_name'], scores=driver['scores']),
                                 reply_markup=get_driver_menu())
            await state.set_state("driver_menu")
            await state.update_data({'current_driver': driver, 'current_cart': current_cart})
            return
        employee = get_employee_by_user_id(user['id'])
        if employee:
            await message.answer(texts["select_action"], reply_markup=get_employee_menu())
            await state.set_state("employee_menu")
            await state.update_data({'current_employee': employee})
            return

    if user is None:
        from_user = message.from_user
        user = create_user({'telegram_id': from_user.id, 'telegram_username': from_user.username,
                            'telegram_name': from_user.full_name})

    await state.update_data({'current_user': user})
    await state.set_state("get_number")

    await message.answer(texts["greet_user"].format(user_telegram_name=user_telegram_name),
                         reply_markup=get_contact_registration())


async def get_number_handler(message: types.Message, state: FSMContext):
    if message.content_type not in ('text', 'contact'):
        await message.answer(texts["send_phone_or_contact"], reply_markup=get_contact_registration())
        return

    if message.content_type == 'text':
        if message.text == TEXT_EMPLOYEE:
            await message.answer(texts["request_admin_role"], reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(None)
            return
        if not validate_uzbek_phone_number(message.text):
            await message.answer(texts["invalid_phone_format"], reply_markup=get_contact_registration())
            return
        phone_number = message.text
    elif message.content_type == 'contact':
        phone_number = message.contact.phone_number

    driver = yandex_api.get_driver_by_number(phone_number)
    if driver:
        data = await state.get_data()
        current_user = data.get('current_user')

        yandex_id = driver['driver_profile']['id']
        callsign = driver['car']['callsign']
        phone = driver['driver_profile']['phones'][0]
        first_name = driver['driver_profile']['first_name']
        last_name = driver['driver_profile']['last_name']
        middle_name = driver['driver_profile'].get('middle_name')

        existed_driver = get_driver_by_phone_number(phone)

        if existed_driver:
            driver_user = get_user_by_id(existed_driver['user_id'])
            current_driver = existed_driver

            if existed_driver['yandex_id'] != yandex_id:
                current_driver = update_driver(existed_driver['id'], {'yandex_id': yandex_id, 'callsign': callsign,
                                                                      'first_name': first_name, 'last_name': last_name,
                                                                      'middle_name': middle_name})

            from_user = message.from_user
            if driver_user['telegram_id'] != from_user.id:
                current_driver = update_driver(existed_driver['id'], {'user_id': current_user['id']})
        else:

            current_driver = create_driver(
                {'user_id': current_user['id'], 'phone_number': phone, 'yandex_id': yandex_id, 'callsign': callsign,
                 'first_name': first_name, 'last_name': last_name, 'middle_name': middle_name})

        current_cart = get_cart_by_driver_id(current_driver['id'])
        if not current_cart:
            current_cart = create_cart({'driver_id': current_driver['id']})

        await message.answer(
            texts["greet_driver"].format(first_name=current_driver['first_name'], scores=current_driver['scores']),
            reply_markup=get_driver_menu())
        await state.update_data({'current_driver': current_driver, 'current_cart': current_cart})
        await state.set_state("driver_menu")
    else:
        await message.answer(texts["driver_not_registered"], reply_markup=get_contact_registration())
