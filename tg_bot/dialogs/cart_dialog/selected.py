import betterlogging
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from tg_bot.dialogs.cart_dialog.states import CartStates
from tg_bot.handlers.buy import start_buy
from tg_bot.misc.availablequantity import get_available_quantity
from tg_bot.misc.states import BuyStates


async def on_chosen_item(call: types.CallbackQuery, widget: Select, dialog_manager: DialogManager, item_name: str):
    dialog_manager.dialog_data.update(item_name=item_name)
    await dialog_manager.switch_to(CartStates.item_info)


async def on_refresh_cart(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(CartStates.refresh_cart)


async def on_increase(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    state: FSMContext = dialog_manager.middleware_data.get('state')
    data = await state.get_data()
    cart = data.get("cart")
    session = dialog_manager.middleware_data.get("session")
    item_name = dialog_manager.dialog_data.get("item_name")
    cart[item_name] += 1
    quantity = cart.get(item_name)

    if not await get_available_quantity(session, item_name, quantity):
        await call.answer("Вы пытаетесь добавить товаров данного типа больше, чем у нас есть на складе", show_alert=True)
        return

    await state.update_data(data)


async def on_decrease(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    state: FSMContext = dialog_manager.middleware_data.get('state')
    data = await state.get_data()
    cart = data.get("cart")
    item_name = dialog_manager.dialog_data.get("item_name")
    quantity = cart.get(item_name)
    if quantity == 1:
        cart.pop(item_name)
        await state.update_data(data)
        await dialog_manager.switch_to(CartStates.select_item)
        return
    cart[item_name] -= 1
    await state.update_data(data)


async def on_cancel(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    state: FSMContext = dialog_manager.middleware_data.get("state")
    await state.set_state(state=None)
    await call.message.delete()


async def except_refresh_cart(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    state: FSMContext = dialog_manager.middleware_data.get('state')
    data = await state.get_data()
    cart = data.get("cart")
    cart.clear()
    await state.update_data(data)
    await call.answer("Корзина очищена", show_alert=True)


async def to_cart(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(CartStates.select_item)


async def on_buy(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    summ = dialog_manager.dialog_data.get("summ")

    state: FSMContext = dialog_manager.middleware_data.get("state")
    session = dialog_manager.middleware_data.get("session")
    callback_data = dialog_manager.middleware_data.get("callback_data")
    betterlogging.info(f"{callback_data}")
    data = await state.get_data()
    cart: dict = data.get("cart")

    for item_name, quantity in cart.items():
        if not await get_available_quantity(session, item_name, quantity):
            await call.answer(
                text="К сожалению товара не достаточно на складе, посмотрите актуальное количество в каталоге",
                show_alert=True
            )
            return

    await state.update_data(summ=summ)
    await state.set_state(BuyStates.start_buy)
    await start_buy(call, state, session)
