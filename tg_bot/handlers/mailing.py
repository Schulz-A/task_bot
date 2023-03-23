import asyncio

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructure.database.functions.queries import fetch_all_users

mailing_router = Router()


@mailing_router.callback_query(F.data == "mailing")
async def start_mailing(call: types.CallbackQuery, state: FSMContext):
    start_message = await call.message.answer("Напишите сообщение рассылки")

    await state.update_data(start_message=start_message.message_id)
    await state.set_state("mail_entering")


@mailing_router.message(StateFilter("mail_entering"))
async def send_mail(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    start_message = data.get("start_message")

    start_message = await bot.edit_message_text(
            text=f"Текст Вашего сообщения:\n"
            f"{message.text}",
            chat_id=message.chat.id,
            message_id=start_message,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Отправить", callback_data="mailing_send")],
                    [InlineKeyboardButton(text="Отменить", callback_data="cancel_mailing")]
                ]
            )
    )

    await message.delete()
    await state.update_data(start_message=start_message.message_id, text=message.text)


@mailing_router.callback_query(F.data == "mailing_send")
async def finish_mailing(call: types.CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    data = await state.get_data()
    start_message = data.get("start_message")
    text = data.get("text")
    users = await fetch_all_users(session)

    for user in users:
        await bot.send_message(
            chat_id=user.id,
            text=text
        )

    del_message = await bot.edit_message_text(
        text=f"Ваше сообщение отправленно",
        chat_id=call.message.chat.id,
        message_id=start_message,
    )

    await state.set_state(state=None)
    await asyncio.sleep(2)
    await bot.delete_message(call.message.chat.id, del_message.message_id)


@mailing_router.callback_query(F.data == "cancel_mailing")
async def cancel_mailing(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    start_message = data.get("start_message")

    del_message = await bot.edit_message_text(
        text="Отправка отмененна",
        chat_id=call.message.chat.id,
        message_id=start_message,
    )

    await state.set_state(state=None)
    await asyncio.sleep(2)
    await bot.delete_message(call.message.chat.id, del_message.message_id)
