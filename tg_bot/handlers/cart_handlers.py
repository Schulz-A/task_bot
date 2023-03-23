from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode, ShowMode

from tg_bot.dialogs.cart_dialog.states import CartStates
from tg_bot.filters.allowedfilter import AllowedFilter

cart_router = Router()
cart_router.callback_query.filter(AllowedFilter())


@cart_router.callback_query(F.data == "cart")
async def cart_items(call: types.CallbackQuery, dialog_manager: DialogManager, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart")

    if not cart:
        await call.answer("Корзина пустая")
        return
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.start(CartStates.select_item, mode=StartMode.RESET_STACK)
