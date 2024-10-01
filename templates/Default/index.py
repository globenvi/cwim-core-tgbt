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
            NavigationDrawerDestination(
                label="Item 1",
                icon=icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=Icon(icons.DOOR_BACK_DOOR),
            ),
            Divider(thickness=2),
            NavigationDrawerDestination(
                icon_content=Icon(icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=icons.MAIL,
            ),
            NavigationDrawerDestination(
                icon_content=Icon(icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=icons.PHONE,
            ),
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
