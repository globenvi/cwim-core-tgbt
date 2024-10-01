from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM

    def handle_expansion_tile_change(e):
        page.open(
            SnackBar(
                Text(f"ExpansionTile was {'expanded' if e.data == 'true' else 'collapsed'}"),
                duration=1000,
            )
        )
        if e.control.trailing:
            e.control.trailing.name = (
                icons.ARROW_DROP_DOWN
                if e.control.trailing.name == icons.ARROW_DROP_DOWN_CIRCLE
                else icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    drawer = NavigationDrawer(
        controls=[
            Container(height=12),
            # ExpansionTile(
            #     title=Text("ExpansionTile 1"),
            #     subtitle=Text("Trailing expansion arrow icon"),
            #     affinity=TileAffinity.PLATFORM,
            #     maintain_state=True,
            #     collapsed_text_color=colors.ON_PRIMARY,
            #     text_color=colors.ON_PRIMARY,
            #     controls=[
            #         ListTile(
            #             title=Text("This is sub-tile number 1")
            #         )
            #     ],
            # ),
            Divider(thickness=2),
            NavigationDrawer(
                icon_content=Icon(icons.VERIFIED_USER),
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
