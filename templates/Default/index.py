from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    drawer = NavigationDrawer(
        controls=[
            Container(height=12),
            TextButton(text="Item 1"),
            Divider(thickness=2),
        ],
    )
    page.appbar = AppBar(
        leading=IconButton(icons.MENU, on_click=lambda e: page.open(drawer)),
        leading_width=40,
        title=Text('SourceSMS', color=colors.ON_PRIMARY),
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
