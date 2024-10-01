from flet import *

def tpl_index(page: Page):
    page.vertical_alignment = "start"

    header = AppBar(
        title=Text("SRC CMS"),
        bgcolor="#1976D2",
        color="#FFFFFF"
    )

    def menu_clicked(e):
        print(f"Menu item clicked: {e.control.selected_index}")

    rail = NavigationRail(
        destinations=[
            NavigationRailDestination(
                icon=icons.ADMIN_PANEL_SETTINGS_OUTLINED, selected_icon=icons.ADMIN_PANEL_SETTINGS_ROUNDED, label="Админ Панель"
            ),
            NavigationRailDestination(
                icon=icons.PERSON, selected_icon=icons.PERSON, label="Profile"
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED, selected_icon=icons.SETTINGS, label="Settings"
            ),
            NavigationRailDestination(
                icon=icons.LOGOUT, selected_icon=icons.LOGOUT, label="Logout" if page.session.get('user_group') != "guest" else "Войти"
            ),
        ],
        on_change=lambda e: menu_clicked(e),
    )

    content = Column(
        controls=[
            Text('Body!')
        ],
        alignment=MainAxisAlignment.CENTER,
        scroll=True,
        expand=True,
    )

    footer = Container(
        content=Text("© 2024 Home Page"),
        padding=10,
        alignment=alignment.center
    )

    return Column(
        controls=[
            header,
            Row(
                [
                    rail,
                    VerticalDivider(width=1),
                    content,
                ],
                expand=True,
            ),
            footer
        ]
    )
