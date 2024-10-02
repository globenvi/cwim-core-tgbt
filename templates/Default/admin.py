from flet import *

def tpl_admin(page: Page):
    page.title = "Админ Панель"

    user_group = page.session.get('user_group')

    def handle_dismissal(e):
        page.add(Text("Drawer dismissed"))

    def handle_change(e):
        page.add(Text(f"Selected Index changed: {e.selected_index}"))
        # page.close(drawer)
    
    btn = ElevatedButton("Show drawer", on_click=lambda e: page.open(drawer))

    drawer = NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
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

    header = AppBar(
        title=Text("SRC-CMS | Admin"),
        bgcolor=colors.PRIMARY,
        color=colors.ON_PRIMARY,
        leading=IconButton(icon=icons.MENU, on_click=lambda e: page.open(drawer)),
        actions=[  # Элементы справа
            IconButton(
                icon=icons.PERSON,
                tooltip="Профиль",
                on_click=lambda e: page.go("/profile"),
                visible=False if user_group == 'guest' else True
            ),
            IconButton(
                icon=icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                tooltip="Админ Панель",
                on_click=lambda e: page.go("/admin"),
                visible=False if user_group != 'admin' else True
            ),
        ],
    )


    footer = Container(
        content=Text("© 2024 Admin Panel"),
        padding=10,
        alignment=alignment.center
    )

    return Column(
        scroll=ScrollMode.AUTO,
        controls=[
            header,
            btn,
            drawer

        ]
    )
