from aiogram_dialog import DialogManager

from tg_bot.infrastructure.database.functions.queries import fetch_all_users, fetch_user
from tg_bot.infrastructure.database.models.models import User


async def get_users(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    users = await fetch_all_users(session)

    data = {
        "users": users
    }

    return data


async def get_user_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    user_id = int(dialog_manager.dialog_data.get("user_id"))
    user = await fetch_user(session, User.id == user_id)
    allow = "Разрешен" if user.allow else "Запрещен"

    path = f"users/{user_id}.jpg" if user.photo else f"users/question-mark.jpg"

    dialog_manager.dialog_data.update(allow=user.allow)

    data = {
        "path": path,
        "id": user.id,
        "full_name": user.full_name,
        "allow": allow
    }

    return data
