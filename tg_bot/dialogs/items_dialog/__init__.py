from aiogram_dialog import Dialog

from tg_bot.dialogs.items_dialog.windows import items_window, item_info, change_item


def items_dialog():
    return Dialog(
        items_window(),
        item_info(),
        change_item()
    )
