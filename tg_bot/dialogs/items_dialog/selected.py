import asyncio

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button

from tg_bot.dialogs.items_dialog.states import ItemsGroup
from tg_bot.infrastructure.database.functions.queries import update_item
from tg_bot.infrastructure.database.models.models import Item
from tg_bot.misc.validators import validators


async def on_chosen_item(call: types.CallbackQuery, widget: Select, dialog_manager: DialogManager, item_name: str):
    dialog_manager.dialog_data.update(item_name=item_name)
    await dialog_manager.switch_to(ItemsGroup.item_info)


async def cancel_dialog(call: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    state: FSMContext = dialog_manager.middleware_data.get("state")
    await state.set_state(state=None)
    await call.message.delete()


async def on_chosen_column(call: types.CallbackQuery, widget: Select, dialog_manager: DialogManager, column_name: str):
    dialog_manager.dialog_data.update(column_name=column_name)
    await dialog_manager.switch_to(ItemsGroup.change_column)


async def on_entered(message: types.Message, widget: TextInput, dialog_manager: DialogManager, userprint: str):
    bot: Bot = dialog_manager.middleware_data.get("bot")
    session = dialog_manager.middleware_data.get("session")
    column_name = dialog_manager.dialog_data.get("column_name")
    item_name = dialog_manager.dialog_data.get("item_name")

    try:
        result = validators[column_name](userprint)
    except ValueError as e:
        text = e.args[0]
        del_message = await message.answer(text=text)
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=del_message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=del_message.message_id-2)
        await message.delete()

        return

    await update_item(session, Item.name == item_name, **{column_name: result})
    await message.delete()

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id-1
    )

    del_message = await message.answer("Значение измененно")
    await asyncio.sleep(2)
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=del_message.message_id
    )

    await dialog_manager.switch_to(ItemsGroup.item_info)