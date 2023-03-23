from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, Row, Back
from aiogram_dialog.widgets.text import Format, Const

from tg_bot.dialogs.cart_dialog import states, selected, keyboards, getters


def item_window():
    return Window(
        Format(text="Сумма товаров в корзине {summ}$"),
        keyboards.paginated_items_in_cart(selected.on_chosen_item),
        Button(
            Const("♻️ Очистить корзину"),
            id="refresh_button",
            on_click=selected.on_refresh_cart
        ),
        Button(Const("💰 Оплатить"), id="buy_button", on_click=selected.on_buy),
        Button(Const("❌ Закрыть корзину"), id="cancel_button", on_click=selected.on_cancel),
        state=states.CartStates.select_item,
        getter=getters.get_items_to_cart
    )


def item_info_window():
    return Window(
        Format("{item_name}\n\nКоличество: {quantity}"),
        Group(
            Row(
                Button(Const("➖"), id="decrease_button", on_click=selected.on_decrease),
                Button(Const("➕"), id="increase_button", on_click=selected.on_increase)
            )
        ),
        Back(Const("⬅️ Назад")),
        state=states.CartStates.item_info,
        getter=getters.get_item_info
    )


def refresh_cart_window():
    return Window(
        Format("‼️ Очистить корзину? ‼️"),
        Button(Const("Подтвердить ✅"), id="refresh_except", on_click=selected.except_refresh_cart),
        Button(Const("⬅️ Назад"), id="to_cart_button", on_click=selected.to_cart),
        state=states.CartStates.refresh_cart
    )
