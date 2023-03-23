from aiogram.fsm.state import StatesGroup, State


class UsersGroup(StatesGroup):
    select_user = State()
    user_info = State()