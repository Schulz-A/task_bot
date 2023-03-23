import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_users(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.full_name} ({item.id})"),
            id="users_group",
            item_id_getter=operator.attrgetter("id"),
            items="users",
            on_click=on_click
        ),
        id="scrolling_users",
        width=1, height=5
    )
