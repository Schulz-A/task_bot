from aiogram import Router, F, types
from aiogram_dialog import DialogManager, ShowMode, StartMode

from tg_bot.dialogs.items_dialog.states import ItemsGroup

items_router = Router()


@items_router.callback_query(F.data == "goods")
async def start_items_dialog(call: types.CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.start(ItemsGroup.select_item, mode=StartMode.RESET_STACK)
