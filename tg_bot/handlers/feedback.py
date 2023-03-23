import asyncio

from aiogram import Router, types, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from tg_bot.config import Config
from tg_bot.filters.allowedfilter import AllowedFilter
from tg_bot.keyboards.referralkeyboards import feedback_keyboard

feedback_router = Router()
feedback_router.callback_query.filter(AllowedFilter())


@feedback_router.callback_query(F.data == "feedback")
async def get_feedback(call: types.CallbackQuery, state: FSMContext):
    start_message = await call.message.answer(
        text="Напишите нам Ваш отзыв/предложение/жалобу"
    )

    await state.set_state("entering_feedback")
    await state.update_data(start_message=start_message.message_id)


@feedback_router.message(StateFilter("entering_feedback"))
async def get_feedback_message(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    start_message = data.get("start_message")

    start_message = await bot.edit_message_text(
        f"Ваше сообщение:\n\n"
        f"{message.text}",
        chat_id=message.chat.id,
        message_id=start_message,
        reply_markup=feedback_keyboard
    )

    await message.delete()
    await state.update_data(feedback_text=message.text, start_message=start_message.message_id)


@feedback_router.callback_query(F.data == "send_feedback")
async def send_feedback(call: types.CallbackQuery, state: FSMContext, bot: Bot, config: Config):
    data = await state.get_data()
    feedback_text = data.get("feedback_text")
    start_message = data.get("start_message")

    for admin in config.tg_bot.admins:
        await bot.send_message(
            text=f"{hbold('Новое сообщение!')}\n\n"
                 f"Текст сообщения:\n"
                 f"{feedback_text}\n\n"
                 f"Автор: id{call.from_user.id}, {call.from_user.full_name}",
            chat_id=admin
        )

    del_message = await bot.edit_message_text(
        text="Ваше сообщение отправленно. Благодарим за обратную связь",
        chat_id=call.message.chat.id,
        message_id=start_message
    )

    await asyncio.sleep(2)
    await bot.delete_message(call.message.chat.id, del_message.message_id)
    await state.set_state(state=None)


@feedback_router.callback_query(F.data == "cancel_feedback")
async def cancel_feedback(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    start_message = data.get("start_message")

    del_message = await bot.edit_message_text(
        text="Отправка отмененна",
        chat_id=call.message.chat.id,
        message_id=start_message
    )

    await state.set_state(state=None)
    await asyncio.sleep(3)
    await bot.delete_message(call.from_user.id, del_message.message_id)
