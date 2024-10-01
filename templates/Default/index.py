from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM

    def handle_change(e: ControlEvent):
        print(f"change on panel with index {e.data}")

    panel = ExpansionPanelList(
        expand_icon_color=colors.AMBER,
        elevation=8,
        divider_color=colors.AMBER,
        on_change=handle_change,
        controls=[
            ExpansionPanel(
                # has no header and content - placeholders will be used
                bgcolor=colors.BLUE_400,
                expanded=True,
            )
        ]
    )

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    drawer = NavigationDrawer(
        controls=[
            Container(height=12),
            ExpansionPanel(
                bgcolor=colors.ON_PRIMARY,
                header=ListTile(title=Text(f"Panel name")),
            )
            ,
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
