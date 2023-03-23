from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from tg_bot.dialogs.users_dialog.states import UsersGroup
from tg_bot.infrastructure.database.functions.queries import update_user
from tg_bot.infrastructure.database.models.models import User


async def on_chosen_user(call: types.CallbackQuery, widget: Select, dialog_manager: DialogManager, user_id):
    dialog_manager.dialog_data.update(user_id=user_id)
    await dialog_manager.switch_to(UsersGroup.user_info)


async def exit_users_dialog(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    state: FSMContext = dialog_manager.middleware_data.get("state")
    await state.set_state(state=None)
    await call.message.delete()


async def on_allow(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data.get("session")
    allow = dialog_manager.dialog_data.get("allow")
    user_id = int(dialog_manager.dialog_data.get("user_id"))

    await update_user(session, User.id == user_id, allow=not allow)
