from aiogram.filters.callback_data import CallbackData


class ItemCB(CallbackData, prefix='item'):
    action: str
    id: int