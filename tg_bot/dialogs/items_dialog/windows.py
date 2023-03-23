from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const

from tg_bot.dialogs.items_dialog import keyboards, selected, getters, states


def items_window():
    return Window(
        Format("Меню изменения товаров"),
        keyboards.paginated_items(selected.on_chosen_item),
        Button(Const("Назад"), id="cancel_items_dialog", on_click=selected.cancel_dialog),
        getter=getters.get_items,
        state=states.ItemsGroup.select_item
    )


def item_info():
    return Window(
        StaticMedia(
            url=Format("{url}")
        ),
        Format(
            "Название товара: {name}\n\n"
            "Описание:\n"
            "{descr}\n\n"
            "Цена: {price}\n"
            "Колличество: {quantity}"
        ),
        keyboards.column_select(selected.on_chosen_column),
        Back(Const("Назад")),
        getter=getters.get_item_info,
        state=states.ItemsGroup.item_info
    )


def change_item():
    return Window(
        Const("Напишите новое значение"),
        TextInput(
            id="entering",
            on_success=selected.on_entered
        ),
        Back(Const("Назад")),
        state=states.ItemsGroup.change_column
    )
