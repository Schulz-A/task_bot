from aiogram import Router, F, types
from aiogram_dialog import DialogManager, ShowMode, StartMode

from tg_bot.dialogs.users_dialog.states import UsersGroup

users_router = Router()


@users_router.callback_query(F.data == "users")
async def start_users_dialog(call: types.CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.start(UsersGroup.select_user, mode=StartMode.RESET_STACK)
