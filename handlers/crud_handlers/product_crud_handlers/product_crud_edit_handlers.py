from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callbacks.crud_callbacks.product_crud_callbacks import ProductAddCallbackData, \
    ProductEditCallbackData
from functions.product_crud import update_product
from handlers.crud_handlers.product_crud_handlers.product_crud_config import texts, answer_texts

from handlers.crud_handlers import answer_resend
from keyboards.inline.crud_keyboards.product_crud_keyboards import (
    product_edit_keyboard,
    product_back_to_keyboard,
)


async def product_edit_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для выбора редактируемого поля продукта.
    """
    message_id = (await state.get_data()).get('message_id')
    print(message_id)
    await answer_resend(callback_query.message, message_id, False, texts['product_edit'], product_edit_keyboard())


async def product_edit_field_handler(callback_query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    """
    Обработчик для редактирования конкретного поля продукта.
    """
    data = await state.get_data()
    product = data['product']

    if callback_data.field == 'title':
        text = texts['product_edit_title'].format(title=product['title'])
        await state.set_state('product_edit_title')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductEditCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})

    elif callback_data.field == 'money_price':
        text = texts['product_edit_money_price'].format(money_price=product['money_price'])
        await state.set_state('product_edit_money_price')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})

    elif callback_data.field == 'score_price':
        text = texts['product_edit_score_price'].format(score_price=product['score_price'])
        await state.set_state('product_edit_score_price')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})

    elif callback_data.field == 'image':
        text = texts['product_edit_image'].format(image=product['image'])
        await state.set_state('product_edit_image')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})

    elif callback_data.field == 'description':
        text = texts['product_edit_description'].format(description=product['description'])
        await state.set_state('product_edit_description')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': callback_query.message.message_id})


async def product_edit_title_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    title = message.text
    product = data['product']
    update_product(product['id'], {'title': title})
    answer_text = answer_texts['product_update_title'].format(title=title)

    msg = await answer_resend(message, message_id, answer_text, texts['product_edit'], product_edit_keyboard())
    await state.update_data({'message_id': msg})


async def product_edit_money_price_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    try:
        money_price = float(message.text)
    except ValueError:
        answer_text = answer_texts['number_only']
        text = texts['product_add_money_price']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': msg})
    else:
        product = data['product']
        update_product(product['id'], {'money_price': money_price})
        answer_text = answer_texts['product_update_money_price'].format(money_price=money_price)

        msg = await answer_resend(message, message_id, answer_text, texts['product_edit'], product_edit_keyboard())
        await state.update_data({'message_id': msg})


async def product_edit_score_price_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    try:
        score_price = float(message.text)
    except ValueError:
        answer_text = answer_texts['number_only']
        text = texts['product_add_score_price']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': msg})
    else:
        product = data['product']
        update_product(product['id'], {'score_price': score_price})
        answer_text = answer_texts['product_update_score_price'].format(score_price=score_price)

        msg = await answer_resend(message, message_id, answer_text, texts['product_edit'], product_edit_keyboard())
        await state.update_data({'message_id': msg})


async def product_edit_image_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')

    if message.photo:
        image_id = message.photo[-1].file_id
    else:
        await message.answer("Пожалуйста, отправьте фотографию.")
        return

    product = data['product']
    update_product(product['id'], {'image': image_id})
    answer_text = answer_texts['product_update_image'].format(image=image_id)

    msg = await answer_resend(message, message_id, answer_text, texts['product_edit'], product_edit_keyboard())
    await state.update_data({'message_id': msg})


async def product_edit_description_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    description = message.text
    product = data['product']
    update_product(product['id'], {'description': description})
    answer_text = answer_texts['product_update_description'].format(description=description)

    msg = await answer_resend(message, message_id, answer_text, texts['product_edit'], product_edit_keyboard())
    await state.update_data({'message_id': msg})

