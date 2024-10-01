from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = AppBar(
        leading=Icon(icons.PALETTE),
        leading_width=40,
        title=Text("AppBar Example", color=colors.ON_PRIMARY),
        center_title=False,
        bgcolor=colors.PRIMARY,
        actions=[
            IconButton(icons.WB_SUNNY_OUTLINED),
            IconButton(icons.FILTER_3),
            PopupMenuButton(
                items=[
                    PopupMenuItem(text="Item 1"),
                    PopupMenuItem(),  # divider
                    PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )
    page.add(Text("Body!"))
