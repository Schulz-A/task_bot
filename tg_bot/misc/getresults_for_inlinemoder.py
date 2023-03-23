from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, hitalic, hide_link
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructure.database.functions.queries import get_all_items, get_items_by
from tg_bot.keyboards.callbackdata import ItemCB


async def get_results_for_im(session: AsyncSession, text: str):
    if len(text) < 2:
        items = await get_all_items(session)
    else:
        items = await get_items_by(session, text)
    results = [types.InlineQueryResultArticle(
        id=item.id,
        title=item.name,
        description=str(item.price) + "$",
        caption=item.name,
        thumb_url=item.photo_id,
        photo_url=item.photo_id,
        input_message_content=types.InputTextMessageContent(
            message_text=f"{hbold(item.name)}\n\n"
                         f"{hitalic(item.descr)}\n\n"
                         f"Цена: {item.price}$\n"
                         f"Доступное количество: {item.quantity}"
                         f"{hide_link(item.photo_id)}"

        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить товар", callback_data=ItemCB(action="add", id=item.id).pack())],
            [InlineKeyboardButton(text="Отменить", callback_data="get_out")]
        ])
    ) for item in items if item.quantity > 0]

    return results
