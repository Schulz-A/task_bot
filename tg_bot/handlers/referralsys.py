import asyncio

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.filters.allowedfilter import AllowedFilter
from tg_bot.infrastructure.database.functions.queries import fetch_user, update_user
from tg_bot.infrastructure.database.models.models import User
from tg_bot.keyboards.referralkeyboards import ref_keyboard

referral_router = Router()
referral_router.callback_query.filter(AllowedFilter())


@referral_router.callback_query(F.data == "referral")
async def referral_menu(call: types.CallbackQuery, session: AsyncSession):
    user = await fetch_user(session, User.id == call.from_user.id)

    await call.message.edit_text(
        text=f"{hbold('Меню реферальной системы')}\n\n"
             f"У Вас {user.bounty}$ бонусов, которыми Вы можете воспользоваться при покупке товаров.\n\n"
             f"Так же Вы можете задать код приглашения",
        reply_markup=ref_keyboard
    )


@referral_router.callback_query(F.data == "set_ref_code")
async def entering_new_code(call: types.CallbackQuery, state: FSMContext):
    del_message = await call.message.answer("Ведите код")
    await state.update_data(message_id=del_message.message_id)
    await state.set_state("entering_new_code")


@referral_router.message(StateFilter("entering_new_code"))
async def validate_new_code(message: types.Message, session: AsyncSession, state: FSMContext, bot: Bot):
    new_code = message.text
    user = await fetch_user(session, User.referral_code == new_code)

    if len(new_code) < 5:
        del_message = await message.answer("Код должен состоять минимуи из 5 символов. Попробуйте еще раз")
        await asyncio.sleep(2)
        await bot.delete_message(message.chat.id, del_message.message_id)
        await message.delete()
        return
    if user:
        del_message = await message.answer("Такой код уже существует. Попробуйте еще раз")
        await asyncio.sleep(2)
        await bot.delete_message(message.chat.id, del_message.message_id)
        await message.delete()
        return

    data = await state.get_data()
    message_id = data.get("message_id")

    del_message = await bot.edit_message_text(
        text="Ваш код успешно изменен",
        chat_id=message.chat.id,
        message_id=message_id
    )

    await update_user(session, User.id == message.from_user.id, referral_code=new_code)

    await asyncio.sleep(3)
    await bot.delete_message(message.chat.id, del_message.message_id)
    await message.delete()

    await state.set_state(state=None)
