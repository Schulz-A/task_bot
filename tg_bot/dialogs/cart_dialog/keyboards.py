import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_items_in_cart(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[0]} ({item[1]})"),
            id="items_group",
            item_id_getter=operator.itemgetter(0),
            items="items",
            on_click=on_click
        ),
        id="scrolling_items",
        width=1, height=5
    )
