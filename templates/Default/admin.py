from flet import *

def tpl_admin(page: Page):
    page.title = "Админ Панель"
    page.vertical_alignment = "start"

    # Функция для возврата на предыдущую страницу
    def go_back(e):
        page.go(-1)  # Возвращаемся на предыдущую страницу

    # Проверяем, находится ли пользователь на стартовой странице
    is_start_page = page.route in ["/index", "/"]

    # AppBar с проверкой на стартовую страницу. Если это не стартовая страница, показываем кнопку "Назад".
    header = AppBar(
        title=Text("SRC CMS"),
        bgcolor=colors.PRIMARY,
        color=colors.ON_PRIMARY,
        leading=IconButton(  # Кнопка "Назад", прикреплённая к левой части AppBar
            icon=icons.ARROW_BACK,
            tooltip="Назад",
            on_click=go_back  # Обработчик нажатия для возврата назад
        ) if not is_start_page else None,  # Скрываем кнопку "Назад" на стартовой странице
        actions=[  # Элементы справа
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

