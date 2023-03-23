from aiogram_dialog import DialogRegistry

from tg_bot.dialogs.cart_dialog import cart_dialog
from tg_bot.dialogs.items_dialog import items_dialog
from tg_bot.dialogs.users_dialog import users_dialog


def register_all_dialogs(dp):
    registry = DialogRegistry(dp=dp)

    for dialog in [
        cart_dialog(),
        users_dialog(),
        items_dialog()
    ]:
        registry.register(dialog)

