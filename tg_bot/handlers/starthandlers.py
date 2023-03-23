from typing import Union

from aiogram import Router, types, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.filters.allowedfilter import AllowedFilter
from tg_bot.infrastructure.database.functions.queries import add_user, fetch_user, update_user
from tg_bot.infrastructure.database.models.models import User
from tg_bot.keyboards.startkeyboard import start_keyboard, enter_code_keyboard, main_menu_button
from tg_bot.misc.getresults_for_inlinemoder import get_results_for_im

start_router = Router()
start_router.message.filter(AllowedFilter())
start_router.callback_query.filter(AllowedFilter())
start_router.inline_query.filter(AllowedFilter())


@start_router.callback_query(F.data == "main")
@start_router.message(Command('start'), AllowedFilter())
async def start_for_allowed(update: Union[types.Message, types.CallbackQuery], event_from_user, session: AsyncSession,
                            state: FSMContext, bot: Bot, **kwargs):
    message = update.message if type(update) == types.CallbackQuery else update
    user = await fetch_user(session, User.id == event_from_user.id)

    if not user:
        chat = await bot.get_chat(message.chat.id)
        photo = chat.photo
        if photo:
            photo = photo.big_file_id
            await bot.download(photo, f"users/{chat.id}.jpg")
            photo = True
        else:
            photo = False
        await add_user(session, event_from_user.id, event_from_user.username,
                       event_from_user.full_name, allow=True, photo=photo)

    referral_text = "У Вас нет пригласительного кода, задать его можно в разделе рефералка"
    referral_code = referral_text if not user or not user.referral_code else user.referral_code

    text = f"{hbold('Приветствую в нашем магазине!')}\n\n" \
           f"Вы можете получить бонус в 10$, если пригласите рефералов.\n\n" \
           f"Ваша реферальная ссылка: https://t.me/Testtotesttotest_bot?start={event_from_user.id}\n\n" \
           f"Ваш код приглашения: {referral_code}" \

    command = kwargs.get('command')

    if command:
        await message.answer(text=text, reply_markup=start_keyboard)
    else:
        await message.edit_text(text=text, reply_markup=start_keyboard)

    data = await state.get_data()
    cart = data.get("cart", {})
    data.clear()
    data.update(cart=cart)
    await state.set_data(data)


@start_router.message(CommandStart(deep_link=True))
async def start_for_deep_link(message: types.Message, session: AsyncSession):
    text = message.text
    if not text.startswith('/start'):
        await message.answer(f"Диплинка не существует")

    try:
        deep_link_id = int(text.split()[-1])
        user_referrer = await fetch_user(session, User.id == deep_link_id)
        if not user_referrer or not user_referrer.allow:
            raise ValueError
    except ValueError:
        await message.answer(f"Реферальной ссылки не существует\n"
                             f"Чтобы  использовать бота введитекод приглашения,\n"
                             f"либо пройдите по реферальной ссылке.",
                             reply_markup=enter_code_keyboard
                             )
        return

    await update_user(session, User.id == deep_link_id, bounty=User.bounty + 10)

    await message.answer(f"{hbold('Вы получили доступ к магазину')}\n"
                         f"Вас пригласил: {user_referrer.full_name}\n\n"
                         f"Чтобы продолжить нажмите на кнопку",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[[main_menu_button]])
                         )


@start_router.message(CommandStart())
async def start_for_default(message: types.Message):
    await message.answer(f"Ошибка!\n"
                         f"У Вас нет доступа.\n"
                         f"Чтобы  использовать бота введите код приглашения,\n"
                         f"либо пройдите по реферальной ссылке.",
                         reply_markup=enter_code_keyboard)


@start_router.callback_query(F.data == "enter_code")
async def enter_code(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Введите код")
    await state.set_state("entering_code")


@start_router.message(StateFilter("entering_code"))
async def excepting_code(message: types.Message, event_from_user, session: AsyncSession, state: FSMContext,
                         bot: Bot, **kwargs):
    code = message.text.strip()
    user = await fetch_user(session, User.referral_code == code)
    if not user:
        await message.answer("Код не существует")
        return

    await update_user(session, User.referral_code == code, bounty=User.bounty + 10)
    kwargs['command'] = "xxx"
    await state.clear()
    await start_for_allowed(message, event_from_user, session, state, bot, **kwargs)


@start_router.inline_query()
async def items_inline(query: types.InlineQuery, session: AsyncSession):
    text = query.query
    await query.answer(results=await get_results_for_im(session, text), cache_time=5)
