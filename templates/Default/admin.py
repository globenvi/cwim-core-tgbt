from flet import *

def tpl_admin(page: Page):
    page.title = "Админ Панель"
    page.vertical_alignment = "start"

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
                visible=False if user_group != 'admin' else True  # Укажите путь к админ панели
            ),
        ],
    )

    def menu_clicked(e):
        if e.control.selected_index == 5:  # Кнопка "Logout"
            if user_group != "guest":
                page.session.clear()  # Очищаем сессию при выходе
                page.go("/login")  # Переход на страницу авторизации
            else:
                page.go("/login")  # Переход на страницу авторизации
        elif e.control.selected_index == 0:  # Кнопка "Управление пользователями"
            pass
        elif e.control.selected_index == 1:  # Кнопка "Активные сессии"
            pass # Переход на страницу активных сессий
        elif e.control.selected_index == 2:  # Кнопка "Управление модулями"
            pass  # Переход на страницу управления модулями
        elif e.control.selected_index == 3:  # Кнопка "Настройки системы"
            pass # Переход на страницу настроек системы

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

    # Основное содержимое админки
    content = Column(
        controls=[
            Text('Добро пожаловать в админ-панель!', size=20),
            Text('Здесь вы можете управлять системой.', size=16)
        ],
        alignment=MainAxisAlignment.START,
        scroll=True,
        expand=True,
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
                    VerticalDivider(width=1),
                    content,
                ],
                expand=True,
            ),
            footer
        ]
    )

