from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_button = InlineKeyboardButton(text="🗂️ Главное меню", callback_data="main")

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✉ Каталог", switch_inline_query_current_chat=""),
        InlineKeyboardButton(text="📕 Обратная связь", callback_data="feedback")
    ],
    [
        InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")
    ],
    [
        InlineKeyboardButton(text="🌐 Рефералка", callback_data="referral")
    ],
    [
        InlineKeyboardButton(text="🎛 Панель администратора", callback_data="admin_panel")
    ]
])

enter_code_keyboard = InlineKeyboardMarkup(
                             inline_keyboard=[[InlineKeyboardButton(
                                 text="🔑 Ввести код", callback_data="enter_code"
                             )
                             ]
                             ]
)

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🎁 Добавить товар", callback_data="add_item"),
        InlineKeyboardButton(text="📢 Рассылка", callback_data="mailing")
    ],
    [
        InlineKeyboardButton(text="👥 Пользователи", callback_data="users")
    ],
    [
        InlineKeyboardButton(text="🗃️ Товары", callback_data="goods")
    ],
    [
        main_menu_button
    ]
])

