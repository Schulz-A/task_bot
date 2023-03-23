from aiogram_dialog import DialogManager

from tg_bot.infrastructure.database.functions.queries import get_all_items, get_item
from tg_bot.infrastructure.database.models.models import Item


async def get_items(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    items = await get_all_items(session)

    data = {
        "items": items
    }

    return data


async def get_item_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    item_name = dialog_manager.dialog_data.get("item_name")
    item: Item = await get_item(session, Item.name == item_name)
    coll_names = [("Название", "name"), ("Описание", "descr"), ("Цена", "price"), ("Колличество", "quantity")]

    data = {
        "url": item.photo_id,
        "name": item.name,
        "descr": item.descr,
        "price": item.price,
        "quantity": item.quantity,
        "coll_names": coll_names
    }

    return data
