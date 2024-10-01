from flet import *

def tpl_index(page: Page):
    page.vertical_alignment = "start"

    header = AppBar(
        title=Text("SRC CMS"),
        bgcolor="#1976D2",
        color="#FFFFFF",
        actions=[
            IconButton(
                icon=icons.PERSON,
                tooltip="Профиль",
                on_click=lambda e: page.go("/profile")  # Укажите путь к странице профиля
            ),
            IconButton(
                icon=icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                tooltip="Админ Панель",
                on_click=lambda e: page.go("/admin")  # Укажите путь к админ панели
            ),
        ],
    )

    user_group = page.session.get('user_group')  # Получаем группу пользователя

    def menu_clicked(e):
        if e.control.selected_index == 5:  # Кнопка "Logout"
            if user_group != "guest":
                page.session.clear()  # Удаляем значения в сессии
                page.go("/index")  # Переходим на страницу авторизации
            else:
                page.go("/login")  # Переходим на страницу авторизации

    rail = NavigationRail(
        destinations=[
            NavigationRailDestination(
                icon=icons.HOME,
                selected_icon=icons.HOME,
                label="Главная"
            ),
            NavigationRailDestination(
                icon=icons.CABLE_OUTLINED,
                selected_icon=icons.CABLE_OUTLINED,
                label="Серверы"
            ),
            NavigationRailDestination(
                icon=icons.LOCK,
                selected_icon=icons.LOCK,
                label="Список банов"
            ),
            NavigationRailDestination(
                icon=icons.VOICE_OVER_OFF,
                selected_icon=icons.VOICE_OVER_OFF,
                label="Список Мутов/Гагов"
            ),
            NavigationRailDestination(
                icon=icons.STAR_HALF,
                selected_icon=icons.STAR_HALF,
                label="Админ-лист"
            ),

            NavigationRailDestination(
                icon=icons.LOGOUT if user_group != "guest" else icons.LOGIN,  # Меняем иконку в зависимости от группы
                selected_icon=icons.LOGOUT if user_group != "guest" else icons.LOGIN,
                label="Logout" if user_group != "guest" else "Войти",  # Меняем текст в зависимости от группы
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
