from flet import *

def tpl_admin(page: Page):
    page.title = "Админ Панель"

    user_group = page.session.get('user_group')

    header = AppBar(
        title=Text("SRC-CMS | Admin"),
        bgcolor=colors.PRIMARY,
        color=colors.ON_PRIMARY,
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

    # Начальное содержимое админки
    body_content = Column(
        controls=[
            Text('Добро пожаловать в админ-панель!', size=20),
            Text('Здесь вы можете управлять системой.', size=16)
        ],
        # alignment=MainAxisAlignment.START,
        scroll=True,
        expand=True,
    )

    def update_body_content(content_controls):
        body_content.controls.clear()  # Очистка текущего содержимого
        body_content.controls.extend(content_controls)  # Обновление содержимого
        page.update()

    def menu_clicked(e):
        if e.control.selected_index == 5:  # Кнопка "Logout"
            if user_group != "guest":
                page.session.clear()  # Очищаем сессию при выходе
                page.go("/login")  # Переход на страницу авторизации
            else:
                page.go("/login")  # Переход на страницу авторизации
        elif e.control.selected_index == 0:  # Кнопка "Управление пользователями"
            users = ["User1", "User2", "User3"]  # Пример списка пользователей
            update_body_content([
                Container(
                    bgcolor=colors.ON_SECONDARY,
                    padding=20,
                    expand=True,
                    height=300,
                    # alignment=alignment.top_left
                )
            ])
        elif e.control.selected_index == 1:  # Кнопка "Активные сессии"
            update_body_content([Text("Список активных сессий", size=18)])  # Заменить содержимым активных сессий
        elif e.control.selected_index == 2:  # Кнопка "Управление модулями"
            update_body_content([Text("Управление модулями", size=18)])  # Заменить содержимым для модулей
        elif e.control.selected_index == 3:  # Кнопка "Настройки системы"
            update_body_content([Text("Настройки системы", size=18)])  # Заменить содержимым настроек

    # Навигационное меню
    rail = NavigationRail(
        destinations=[
            NavigationRailDestination(
                icon=icons.PEOPLE_OUTLINE,
                selected_icon=icons.PEOPLE,
                label="Управление пользователями"
            ),
            NavigationRailDestination(
                icon=icons.MONITOR_HEART,
                selected_icon=icons.MONITOR_HEART,
                label="Активные сессии"
            ),
            NavigationRailDestination(
                icon=icons.EXTENSION_OUTLINED,
                selected_icon=icons.EXTENSION,
                label="Управление модулями"
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon=icons.SETTINGS,
                label="Настройки системы"
            ),
            NavigationRailDestination(
                icon=icons.LOGOUT if user_group != "guest" else icons.LOGIN,
                selected_icon=icons.LOGOUT if user_group != "guest" else icons.LOGIN,
                label="Logout" if user_group != "guest" else "Войти",
            ),
        ],
        on_change=lambda e: menu_clicked(e),
    )

    footer = Container(
        content=Text("© 2024 Admin Panel"),
        padding=10,
        alignment=alignment.center
    )

    return Column(
        controls=[
            header,
            Row(
                [
                    rail,
                    VerticalDivider(width=2),
                    body_content,
                ],
                expand=True,
            ),
            footer
        ]
    )
