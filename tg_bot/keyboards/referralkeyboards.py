from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.startkeyboard import main_menu_button

ref_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔒 Установить код", callback_data="set_ref_code")],
        [main_menu_button]
    ]
)

feedback_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить", callback_data="send_feedback")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_feedback")]
    ]
)
