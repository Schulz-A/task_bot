from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

except_buy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Подтвердить", callback_data="exception_buy")],
    [InlineKeyboardButton(text="🪙 Воспользоваться бонусами", callback_data="bounty_use")],
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_buying")]
])

finish_buy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧾 Я оплатил", callback_data="check_payment")],
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_buying")]
])

except_buy_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Подтвердить", callback_data="exception_buy")],
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_buying")]
])
