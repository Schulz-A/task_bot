from aiogram.fsm.context import FSMContext

from aiogram_dialog import DialogManager

from tg_bot.infrastructure.database.functions.queries import get_item
from tg_bot.infrastructure.database.models.models import Item


async def get_items_to_cart(dialog_manager: DialogManager, **middleware_data):
    summ = 0

    state: FSMContext = middleware_data.get('state')
    state_data = await state.get_data()
    cart = state_data.get("cart")
    session = middleware_data.get('session')
    cart_items = cart.items()

    for name, quantity in cart.items():
        item = await get_item(session, Item.name == name)
        if item:
            summ += item.price * quantity

    dialog_manager.dialog_data.update({"summ": summ})

    data = {
        "items": cart_items,
        "summ": summ
    }

    return data


async def get_item_info(dialog_manager: DialogManager, **middleware_data):
    state: FSMContext = middleware_data.get('state')
    data = await state.get_data()
    cart = data.get("cart")
    item_name = dialog_manager.dialog_data.get("item_name")
    quantity = cart.get(item_name)

    data = {
        "item_name": item_name,
        "quantity": quantity
    }

    return data
