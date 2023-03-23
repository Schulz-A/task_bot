import asyncio
from typing import Any


from aiogram import Router, types, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hunderline
from nowpayments.sandbox import NOWPaymentsSandbox
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.config import Config
from tg_bot.infrastructure.database.functions.queries import fetch_user, update_user, update_item
from tg_bot.infrastructure.database.models.models import User, Item
from tg_bot.keyboards.buykeyboards import except_buy_keyboard, finish_buy_keyboard, except_buy_keyboard2
from tg_bot.keyboards.startkeyboard import main_menu_button
from tg_bot.misc.states import BuyStates

buy_router = Router()


@buy_router.callback_query(F.data == "bounty_use")
@buy_router.callback_query(StateFilter(BuyStates.start_buy))
async def start_buy(call: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    summ = data.get('summ')
    keyboard = except_buy_keyboard
    if call.data == "bounty_use":
        keyboard = except_buy_keyboard2
        user = await fetch_user(session, User.id == call.from_user.id)
        summ -= user.bounty
        await state.update_data(summ=summ, bounty=user.bounty)
        await call.answer(f"Было списано {user.bounty}$ бонусов", show_alert=True)

    await call.message.edit_text(text=f"Вы перешли к оплате\n\n"
                                      f"После нажатия на кнопку {hbold('ПОДТВЕРДИТЬ')},"
                                      f"будет сформирован заказ на сумму {summ}$, "
                                      f"который необходимо оплатить через криптовалюту USDT в сети TRC20",
                                 reply_markup=keyboard)
    await state.set_state(state=None)


@buy_router.callback_query(F.data == "exception_buy")
async def excepting_buying(call: types.CallbackQuery, state: FSMContext, payment: NOWPaymentsSandbox):
    data = await state.get_data()
    summ = data.get("summ")
    pay = payment.create_payment(float(summ), 'usd', 'usdttrc20')
    payment_id = pay.get("payment_id")
    pay_address = pay.get("pay_address")

    await call.message.edit_text(
        text=f"Адрес платежа: {hunderline(pay_address)}\n\n"
             f"Сумма платежа: {summ}$\n\n"
             f"После оплаты нажмите {hbold('Я ОПЛАТИЛ')}, "
             f"чтобы проверить статус оплату. "
             f"После того как оплата будет подтверждена, мы сформируем Ваш заказ.\n"
             f"(Оплата подтверждается от 5 до 15 минут)",
        reply_markup=finish_buy_keyboard
    )

    await state.update_data(payment_id=payment_id)


@buy_router.callback_query(F.data == "check_payment")
async def check_payment(call: types.CallbackQuery, state: FSMContext, payment: NOWPaymentsSandbox, bot: Bot,
                        session: AsyncSession):
    data = await state.get_data()
    payment_id = data.get("payment_id")
    payment_check = payment.get_payment_status(payment_id).get("payment_status")
    if payment_check == "waiting":
        await call.answer("Вы не оплатили заказа, либо оплата еще не подтверждена", show_alert=True)
        return
    if payment_check == "finished":
        del_message = await call.message.edit_text(
            text=f"Заказ успешно оплачен.\n"
                 f"Заполните следующую информацию для формирования заказа",
        )

        cart = data.get("cart")

        if data.get("bounty"):
            await update_user(session, User.id == call.from_user.id, bounty=0)

        for item, quantity in cart.items():
            await update_item(session, Item.name == item, quantity=Item.quantity - quantity)

        await bot.send_chat_action(chat_id=call.message.chat.id, action="typing", request_timeout=3)
        await asyncio.sleep(4)
        await bot.delete_message(chat_id=del_message.chat.id, message_id=del_message.message_id)
        del_message = await call.message.answer("Введите ФИО")

        message_id = del_message.message_id
        await state.update_data(message_id=message_id)
        await state.set_state("buyer_info")


@buy_router.message(StateFilter('buyer_info'))
async def buyer_fio(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get("message_id")

    await bot.send_chat_action(chat_id=message.chat.id, action="typing", request_timeout=2)
    await asyncio.sleep(2)

    del_message = await bot.edit_message_text(text="Введите номер телефона",
                                              message_id=message_id,
                                              chat_id=message.chat.id
                                              )
    await message.delete()

    message_id = del_message.message_id
    await state.update_data(message_id=message_id, fio=message.text)
    await state.set_state("entering_phone_number")


@buy_router.message(StateFilter("entering_phone_number"))
async def buyer_phone(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get("message_id")

    await bot.send_chat_action(chat_id=message.chat.id, action="typing", request_timeout=2)
    await asyncio.sleep(2)

    del_message = await bot.edit_message_text(text="Введите адрес",
                                              message_id=message_id,
                                              chat_id=message.chat.id
                                              )

    await message.delete()

    message_id = del_message.message_id
    await state.update_data(message_id=message_id, phone=message.text)
    await state.set_state("entering_address")


@buy_router.message(StateFilter("entering_address"))
async def buyer_address(message: types.Message, state: FSMContext, bot: Bot, config: Config):
    data: dict[str, Any] = await state.get_data()
    message_id = data.get("message_id")

    await bot.send_chat_action(chat_id=message.chat.id, action="typing", request_timeout=2)
    await asyncio.sleep(2)

    await message.delete()

    fio = data.get("fio")
    phone = data.get("phone")
    address = message.text
    cart = data.get("cart")
    items = "\n\n".join((f"Товар: {item}\nКолличество: {quantity}" for item, quantity in cart.items()))

    for admin in config.tg_bot.admins:
        await bot.send_message(
            chat_id=admin,
            text=f"{hbold('НОВЫЙ ЗАКАЗ!!!')}\n\n"
                 f"{items}\n\n\n"
                 f"ФИО покупателя: {fio}\n"
                 f"Номер телефона: {phone}\n"
                 f"Адрес: {address}"
        )

    await state.clear()

    await bot.edit_message_text(text="Спасибо за Ваш заказ, с Вами свяжется наш менеджер для дополнительной информации",
                                message_id=message_id,
                                chat_id=message.chat.id,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[main_menu_button]])
                                )
