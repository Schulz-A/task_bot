import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Column, Group
from aiogram_dialog.widgets.text import Format


def paginated_items(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.name}"),
            id="items_group",
            item_id_getter=operator.attrgetter("name"),
            items="items",
            on_click=on_click
        ),
        id="scrolling_items",
        width=1, height=5
    )


def column_select(on_click):
    return Group(
        Select(
            Format("{item[0]}"),
            id="column_group",
            item_id_getter=operator.itemgetter(1),
            items="coll_names",
            on_click=on_click
        ),
        width=2
    )
