from flet import *

def tpl_index(page: Page):
    page.vertical_alignment = "start"
    user_group = page.session.get('user_group')

    # Функция для смены темы
    def toggle_theme(e):
        if page.theme_mode == "light":
            page.theme_mode = "dark"
        else:
            page.theme_mode = "light"
        page.update()

    # Функция для смены цветовой палитры
    def change_color_palette(e):
        new_color = colors.AMBER if page.bgcolor != colors.AMBER else colors.PRIMARY
        page.bgcolor = new_color
        page.update()

    header = AppBar(
        title=Text("SRC CMS"),
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
            Switch(
                value=page.theme_mode == "dark",
                on_change=toggle_theme,
                label="Темная тема"
            ),
            IconButton(
                icon=icons.COLOR_LENS,
                tooltip="Сменить цветовую палитру",
                on_click=change_color_palette
            ),
        ],
    )

    def menu_clicked(e):
        # Логика навигации
        pass

    rail = NavigationRail(
        destinations=[
            # Элементы навигации
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
