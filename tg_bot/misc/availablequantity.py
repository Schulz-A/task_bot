from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructure.database.functions.queries import get_item
from tg_bot.infrastructure.database.models.models import Item


async def get_available_quantity(session: AsyncSession, item_name: str, quantity: int) -> bool:
    item = await get_item(session, Item.name == item_name)
    if not item or quantity > item.quantity:
        return False
    return True
