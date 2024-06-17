from aiogram.types import Message


async def answer_resend(message: Message, delete_message_id: int, answer_text, text: str, reply_markup):
    await message.bot.delete_message(message.chat.id, delete_message_id)
    if answer_text:
        await message.answer(answer_text)
    msg = await message.answer(text=text, reply_markup=reply_markup)
    return msg.message_id


async def update_message(message: Message, text: str, reply_markup):
    await message.edit_text(text=text, reply_markup=reply_markup)
