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

    user_group = page.session.get('user_group')  # Получаем группу пользователя

    rail = NavigationRail(
        destinations=[
            NavigationRailDestination(
                icon=icons.HOME,
                selected_icon=icons.HOME,
                label="Главная"
            ),
            NavigationRailDestination(
                icon=icons.ROOM_SERVICE,
                selected_icon=icons.ROOM_SERVICE,
                label="Серверы"
            ),
            NavigationRailDestination(
                icon=icons.LOCK,
                selected_icon=icons.LOCK,
                label="Список банов"
            ),
            NavigationRailDestination(
                icon=icons.VOLUME_MUTE,
                selected_icon=icons.VOLUME_MUTE,
                label="Список Мутов/Гагов"
            ),
            NavigationRailDestination(
                icon=icons.LIST,
                selected_icon=icons.LIST,
                label="Админ-лист"
            ),

            NavigationRailDestination(
                icon=icons.LOGOUT if user_group != "guest" else icons.LOGIN,  # Меняем иконку в зависимости от группы
                selected_icon=icons.LOGOUT if user_group != "guest" else icons.LOGIN,
                label="Logout" if user_group != "guest" else "Войти"  # Меняем текст в зависимости от группы
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
