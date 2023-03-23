from aiogram.fsm.state import StatesGroup, State


class BuyStates(StatesGroup):
    start_buy = State()
