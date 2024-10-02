import flet as ft

def tpl_admin(page: ft.Page):
    ft.page.title = "Админ Панель"

    user_group = page.session.get('user_group')

    def handle_dismissal(e):
        ft.page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        ft.page.add(ft.Text(f"Selected Index changed: {e.selected_index}"))
        # page.close(drawer)
    
    btn = ft.ElevatedButton("Show drawer", on_click=lambda e: ft.page.open(drawer))

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )

    header = ft.AppBar(
        title=ft.Text("SRC-CMS | Admin"),
        bgcolor=ft.colors.PRIMARY,
        color=ft.colors.ON_PRIMARY,
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=lambda e: ft.page.open(drawer)),
        actions=[  # Элементы справа
            ft.IconButton(
                icon=ft.icons.PERSON,
                tooltip="Профиль",
                on_click=lambda e: ft.page.go("/profile"),
                visible=False if user_group == 'guest' else True
            ),
            ft.IconButton(
                icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                tooltip="Админ Панель",
                on_click=lambda e: ft.page.go("/admin"),
                visible=False if user_group != 'admin' else True
            ),
        ],
    )


    footer = ft.Container(
        content=ft.Text("© 2024 Admin Panel"),
        padding=10,
        alignment=ft.alignment.center
    )

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            btn,
            drawer

        ]
    )
