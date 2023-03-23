from aiogram.fsm.state import StatesGroup, State


class CartStates(StatesGroup):
    select_item = State()
    item_info = State()
    refresh_cart = State()
