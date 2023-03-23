from aiogram_dialog import Dialog

from tg_bot.dialogs.cart_dialog.windows import item_window, item_info_window, refresh_cart_window


def cart_dialog():
    return Dialog(
        item_window(),
        item_info_window(),
        refresh_cart_window()
    )
