from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Back
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from tg_bot.dialogs.users_dialog import keyboards, selected, getters
from tg_bot.dialogs.users_dialog.states import UsersGroup


def users_window():
    return Window(
        Format("Меню управления пользователями"),
        keyboards.paginated_users(selected.on_chosen_user),
        Button(Const("Назад"), id="exit_user_dialog", on_click=selected.exit_users_dialog),
        getter=getters.get_users,
        state=UsersGroup.select_user
    )


def user_info():
    return Window(
        StaticMedia(
            path=Format("{path}"),
        ),
        Format(
            "Пользователь: {full_name}\n"
            "ID: {id}\n"
            "Доступ: {allow}"
        ),
        Button(Const("Запретить/Разрешить доступ"), id="change_allow", on_click=selected.on_allow),
        Back(Const("Назад")),
        getter=getters.get_user_info,
        state=UsersGroup.user_info
    )
