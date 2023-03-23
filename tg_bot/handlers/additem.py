import asyncio

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructure.database.functions.queries import add_items
from tg_bot.keyboards.add_itemkeyboard import add_item_keyboard
from tg_bot.keyboards.startkeyboard import main_menu_button

add_item = Router()


@add_item.callback_query(F.data == "add_item")
async def start_add_item(call: types.CallbackQuery, state: FSMContext):

    sm = await call.message.answer("Введите название товара")
    await state.update_data(message_id=sm.message_id)
    await state.set_state("enter_name")
    await call.message.delete()


@add_item.message(StateFilter("enter_name"))
async def enter_name(message: types.Message, state: FSMContext, bot: Bot):

    data = await state.get_data()
    message_id = data["message_id"]

    sm = await bot.edit_message_text("Напишите описание товара", chat_id=message.chat.id, message_id=message_id)
    await state.update_data(name=message.text, message_id=sm.message_id)
    await message.delete()
    await state.set_state("enter_descr")


@add_item.message(StateFilter("enter_descr"))
async def enter_descr(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data["message_id"]
    sm = await bot.edit_message_text("Введите колличество товара", chat_id=message.chat.id, message_id=message_id)
    await state.update_data(descr=message.text, message_id=sm.message_id)
    await message.delete()
    await state.set_state("enter_quantity")


@add_item.message(StateFilter("enter_quantity"))
async def enter_quantity(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data["message_id"]
    try:
        quantity = int(message.text)
        await state.update_data(quantity=message.text)
        sm = await bot.edit_message_text("Введите цену товара", chat_id=message.chat.id,
                                         message_id=message_id)

        await state.update_data(quantity=quantity, message_id=sm.message_id)
        await message.delete()
        await state.set_state("enter_price")
    except ValueError:
        err = await message.answer("Введенное значение должно быть числом", disable_notification=True)
        await message.delete()
        await asyncio.sleep(2)
        await err.delete()
        return


@add_item.message(StateFilter("enter_price"))
async def enter_price(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data["message_id"]
    try:
        price = int(message.text)
        sm = await bot.edit_message_text("Пришлите ссылку на фото товара", chat_id=message.chat.id,
                                         message_id=message_id)

        await state.update_data(price=price, message_id=sm.message_id)
        await message.delete()
        await state.set_state("enter_photo_url")
    except ValueError:
        err = await message.answer("Значение должно быть числом")
        await message.delete()
        await asyncio.sleep(2)
        await err.delete()
        return


@add_item.message(StateFilter("enter_photo_url"))
async def result_add_item(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data["message_id"]
    data = await state.get_data()
    item_name = data["name"]
    descr = data["descr"]
    quantity = data["quantity"]
    price = data["price"]
    photo_url = message.text
    await state.update_data(photo_url=photo_url)
    chat_id = message.chat.id

    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    sm = await bot.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=f"Название: {item_name}\n\n"
                f"Количество: {quantity}\n\n"
                f"Цена: {price}$\n\n"
                f"Описание:\n{descr}\n\n",
        reply_markup=add_item_keyboard
    )

    await state.update_data(message_id=sm.message_id)
    await message.delete()


@add_item.callback_query(F.data == "except_add_item")
async def adding_item_to_db(call: types.CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    data = await state.get_data()
    message_id = data["message_id"]
    await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
    data = await state.get_data()
    item_name = data["name"]
    descr = data["descr"]
    quantity = int(data["quantity"])
    price = int(data["price"])
    photo_url = data["photo_url"]
    await add_items(session, item_name, quantity, descr, price, photo_url)

    await state.set_state(state=None)

    await call.message.answer("Вы успешно добавили товар", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
        main_menu_button
    ]]))


@add_item.callback_query(F.data == "cancel_add_item")
async def adding_item_to_db(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data["message_id"]
    await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
    await state.set_state(state=None)

    await call.message.answer("Вы отменили добавление товара", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
        main_menu_button
    ]]))
