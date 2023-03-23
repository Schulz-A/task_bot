from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.filters.viabot import ViaBotFilter
from tg_bot.infrastructure.database.functions.queries import get_item
from tg_bot.infrastructure.database.models.models import Item
from tg_bot.keyboards.callbackdata import ItemCB

item_router = Router()


@item_router.message(ViaBotFilter())
async def cc(message: types.Message, state: FSMContext):
    await state.update_data(message_id=message.message_id, chat_id=message.chat.id)


@item_router.callback_query(F.data == "get_out")
async def m(call: types.CallbackQuery, bot: Bot, state: FSMContext, event_from_user):
    data = await state.get_data()
    mess_id = data["message_id"]
    chat_id = event_from_user.id
    await bot.delete_message(chat_id=chat_id, message_id=mess_id)


@item_router.callback_query(ItemCB.filter(F.action == "add"))
async def items_inline(call: types.CallbackQuery, session: AsyncSession, callback_data: ItemCB,
                       state: FSMContext, bot: Bot, event_from_user):
    item = await get_item(session, Item.id == callback_data.id)
    data = await state.get_data()
    cart = data.get("cart")

    if item.name in cart:
        if cart[item.name] == item.quantity:
            await call.answer("Вы добавили товаров данного типа больше, чем у нас есть на складе", show_alert=True)
            return
        cart[item.name] += 1
    else:
        cart.update({item.name: 1})

    mes_id = data['message_id']
    chat_id = event_from_user.id
    await state.update_data(data)
    await call.answer("Товар добавлен", show_alert=True)

    await bot.delete_message(chat_id, mes_id)
