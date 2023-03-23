from aiogram.fsm.state import StatesGroup, State


class ItemsGroup(StatesGroup):
    select_item = State()
    item_info = State()
    change_column = State()
