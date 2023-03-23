from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

add_item_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить товар", callback_data="except_add_item")],
    [InlineKeyboardButton(text="Отменить", callback_data="cancel_add_item")]
])
