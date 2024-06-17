from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callbacks.crud_callbacks.product_crud_callbacks import ProductAddCallbackData
from functions.product_crud import save_product, remove_product
from keyboards.inline.crud_keyboards.product_crud_keyboards import (
    product_menu_keyboard,
    product_add_keyboard,
    product_back_to_keyboard,
)

from handlers.crud_handlers.product_crud_handlers.product_crud_config import texts, answer_texts

from handlers.crud_handlers import answer_resend


async def product_add_handler(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=texts['product_add'], reply_markup=product_add_keyboard())


async def product_add_field_handler(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    if callback_data.field == 'title':
        text = texts['product_add_title']
        await state.set_state('product_add_title')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))

    elif callback_data.field == 'money_price':
        text = texts['product_add_money_price']
        await state.set_state('product_add_money_price')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))

    elif callback_data.field == 'score_price':
        text = texts['product_add_score_price']
        await state.set_state('product_add_score_price')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))

    elif callback_data.field == 'image':
        text = texts['product_add_image']
        await state.set_state('product_add_image')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))

    elif callback_data.field == 'description':
        text = texts['product_add_description']
        await state.set_state('product_add_description')
        await callback_query.message.edit_text(text=text,
                                               reply_markup=product_back_to_keyboard(ProductAddCallbackData()))


async def product_field_save_handle(message: Message, state: FSMContext, new_product, answer_text, text):
    message_id = (await state.get_data()).get('message_id')

    await state.update_data({'new_product': new_product})

    title = new_product.get('title')
    money_price = new_product.get('money_price')
    score_price = new_product.get('score_price')
    image = new_product.get('image')
    description = new_product.get('description')
    print(message_id)

    msg = await answer_resend(message, message_id, answer_text, text,
                              product_add_keyboard(title, money_price, score_price, image, description))
    await state.update_data({'message_id': msg})


async def product_title_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_product = data.get('new_product')
    title = message.text

    if new_product:
        new_product['title'] = title
    else:
        new_product = {'title': title}

    answer_text = answer_texts['product_add_title'].format(title=title)
    text = texts['product_add']
    await product_field_save_handle(message, state, new_product, answer_text, text)


async def product_money_price_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_product = data.get('new_product')
    try:
        money_price = float(message.text)
    except ValueError:
        answer_text = answer_texts['number_only']
        text = texts['product_add_money_price']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': msg})
    else:
        if new_product:
            new_product['money_price'] = money_price
        else:
            new_product = {'money_price': money_price}

        answer_text = answer_texts['product_add_money_price'].format(money_price=money_price)
        text = texts['product_add']
        await product_field_save_handle(message, state, new_product, answer_text, text)


async def product_score_price_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_product = data.get('new_product')
    try:
        score_price = float(message.text)
    except ValueError:
        answer_text = answer_texts['number_only']
        text = texts['product_add_score_price']
        msg = await answer_resend(message, message_id, answer_text, text,
                                  product_back_to_keyboard(ProductAddCallbackData()))
        await state.update_data({'message_id': msg})
    else:
        if new_product:
            new_product['score_price'] = score_price
        else:
            new_product = {'score_price': score_price}

        answer_text = answer_texts['product_add_score_price'].format(score_price=score_price)
        text = texts['product_add']
        await product_field_save_handle(message, state, new_product, answer_text, text)


async def product_image_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_product = data.get('new_product')

    if message.photo:
        image_id = message.photo[-1].file_id
    else:
        await message.answer("Пожалуйста, отправьте фотографию.")
        return

    if new_product:
        new_product['image'] = image_id
    else:
        new_product = {'image': image_id}

    answer_text = answer_texts['product_add_image']
    text = texts['product_add']
    await product_field_save_handle(message, state, new_product, answer_text, text)


async def product_description_save_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    new_product = data.get('new_product')
    description = message.text

    if new_product:
        new_product['description'] = description
    else:
        new_product = {'description': description}

    answer_text = answer_texts['product_add_description'].format(description=description)
    text = texts['product_add']
    await product_field_save_handle(message, state, new_product, answer_text, text)


async def product_save_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_product: dict = data.get('new_product')
    message_id = data['message_id']

    if new_product:
        title = new_product.get('title')
        money_price = new_product.get('money_price')
        score_price = new_product.get('score_price')
        image = new_product.get('image')
        description = new_product.get('description')
        if title and money_price and score_price and image and description:
            save_product({'title': title, 'money_price': money_price, 'score_price': score_price, 'image': image,
                          'description': description})

            answer_text = texts['product_save']
            msg = await answer_resend(callback_query.message, message_id, answer_text, texts['product_menu'],
                                      product_menu_keyboard())
            await state.set_state(None)
            await state.update_data({'new_product': {}, 'message_id': msg})
            return

        answer_text = texts['product_fill_fields']
        text = texts['product_add']

        await product_field_save_handle(callback_query.message, state, new_product, answer_text, text)


async def product_remove_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = data['product']
    message_id = data['message_id']

    remove_product(product['id'])

    answer_text = texts['product_remove']

    msg = await answer_resend(callback_query.message, message_id, answer_text, texts['product_menu'],
                              product_menu_keyboard())
    await state.update_data({'message_id': msg})
