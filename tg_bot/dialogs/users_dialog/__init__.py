from aiogram_dialog import Dialog

from tg_bot.dialogs.users_dialog.windows import users_window, user_info


def users_dialog():
    return Dialog(
        users_window(),
        user_info()
    )
