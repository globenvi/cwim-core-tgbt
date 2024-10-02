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
        alignment=MainAxisAlignment.START,  # Устанавливаем выравнивание сверху
        scroll=True,  # Добавляем прокрутку
        expand=True,  # Растягиваем контейнер
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

            update_body_content([
                Container(
                    expand=True,
                    alignment=alignment.top_left,
                    content=Column(
                        [
                            Container(
                                bgcolor=colors.PRIMARY,
                                padding=10,
                                expand=True,
                                alignment=alignment.top_left,
                                border_radius=5,
                                content=Text("Управление пользователями", size=18, color=colors.ON_PRIMARY)
                            ),
                            Row(
                                [
                                    Container(
                                        bgcolor=colors.ON_SECONDARY,
                                        expand=True,
                                        alignment=alignment.top_left,
                                        border_radius=5,
                                        height=400,
                                        width=800,
                                        content=DataTable(
                                            show_checkbox_column=True,
                                            sort_ascending=True,
                                            expand_loose=True,
                                            columns=[
                                                DataColumn(Text("ID")),
                                                DataColumn(Text("Логин")),
                                                DataColumn(Text("Email")),
                                                DataColumn(Text("Telegram ID")),
                                                DataColumn(Text("Группа")),
                                                DataColumn(Text("Дата регистрации")),
                                                DataColumn(Text("Действия"))
                                            ],
                                            rows=[
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("1")),
                                                        DataCell(Text("dottenv")),
                                                        DataCell(Text("alexgolubev1404@gmail.com")),
                                                        DataCell(Text("1234567890")),
                                                        DataCell(Text("admin")),
                                                        DataCell(Text("2022-01-01 12:00:00")),
                                                        DataCell(
                                                            Container(content=IconButton(icon=icons.REMOVE_RED_EYE)))
                                                    ],
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("1")),
                                                        DataCell(Text("dottenv")),
                                                        DataCell(Text("alexgolubev1404@gmail.com")),
                                                        DataCell(Text("1234567890")),
                                                        DataCell(Text("admin")),
                                                        DataCell(Text("2022-01-01 12:00:00")),
                                                        DataCell(
                                                            Container(content=IconButton(icon=icons.REMOVE_RED_EYE)))
                                                    ],
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("1")),
                                                        DataCell(Text("dottenv")),
                                                        DataCell(Text("alexgolubev1404@gmail.com")),
                                                        DataCell(Text("1234567890")),
                                                        DataCell(Text("admin")),
                                                        DataCell(Text("2022-01-01 12:00:00")),
                                                        DataCell(
                                                            Container(content=IconButton(icon=icons.REMOVE_RED_EYE)))
                                                    ],
                                                ),
                                            ]
                                        )
                                    ),
                                    # Container(
                                    #     expand=True,
                                    #     bgcolor=colors.ON_SECONDARY,
                                    #     alignment=alignment.top_left,
                                    #     border_radius=5,
                                    #     height=400,
                                    #     width=300
                                    # )
                                ]
                            )
                        ]
                    )
                )
            ])
        elif e.control.selected_index == 1:  # Кнопка "Активные сессии"
            update_body_content([Text("Список активных сессий", size=18)])  # Заменить содержимым активных сессий
        elif e.control.selected_index == 2:  # Кнопка "Управление модулями"
            update_body_content([Text("Управление модулями", size=18)])  # Заменить содержимым для модулей
        elif e.control.selected_index == 3:  # Кнопка "Настройки системы"
            update_body_content([Text("Настройки системы", size=18)])  # Заменить содержимым настроек

    def handle_dismissal(e):
        page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.selected_index}"))
        # page.close(drawer)

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

    footer = Container(
        content=Text("© 2024 Admin Panel"),
        padding=10,
        alignment=alignment.center
    )

    return Column(
        scroll=ScrollMode.AUTO,
        controls=[
            header,
            drawer,
            footer

        ]
    )
