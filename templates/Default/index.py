from flet import *


def tpl_index(page: Page):
    page.vertical_alignment = "start"

    user_group = page.session.get('user_group')

    header = AppBar(
        title=Text("SRC CMS"),
        bgcolor=colors.PRIMARY,
        color=colors.ON_PRIMARY,
        actions=[  # Элементы справа
            IconButton(
                icon=icons.PERSON,
                tooltip="Профиль",
                on_click=lambda e: page.go("/profile"),
                visible=False if user_group == 'guest' else True # Укажите путь к странице профиля
            ),
            IconButton(
                icon=icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                tooltip="Админ Панель",
                on_click=lambda e: page.go("/admin"),
                visible=False if user_group != 'admin' else True # Укажите путь к админ панели
            ),
        ],
    )

    def menu_clicked(e):
        if e.control.selected_index == 5:  # Кнопка "Logout"
            if user_group != "guest":
                page.session.clear()
                page.client_storage.clear()
                page.go("/login")
                page.go('/index')# Переходим на страницу авторизации
                page.update()
            else:
                page.go("/login")  # Переходим на страницу авторизации
        if e.control.selected_index == 0:  # Кнопка "Главная"
            page.go("/index")  # Переходим на страницу главной
        if e.control.selected_index == 1:  # Кнопка "Серверы"
            page.go("/servers")  # Переходим на страницу серверов
        if e.control.selected_index == 2:  # Кнопка "Список банов"
            page.go("/bans")  # Переходим на страницу списка банов
        if e.control.selected_index == 3:  # Кнопка "Список Мутов/Гагов"
            page.go("/mutes")  # Переходим на страницу списка Мутов/Гагов
        if e.control.selected_index == 4:  # Кнопка "Админ-лист"
            page.go("/admin_list")  # Переходим на страницу админ-листа


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
                label="Админ-лист",
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
