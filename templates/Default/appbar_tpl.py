from flet import AppBar, Text, Row, IconButton, icons


def render(page):
    # Создаем AppBar с заголовком и кнопками
    app_bar = AppBar(
        title=Text("Мое приложение"),
        center_title=True,
        leading=IconButton(icons.MENU, tooltip="Меню", on_click=lambda e: page.go("/menu")),
        actions=[
            IconButton(icons.SETTINGS, tooltip="Настройки", on_click=lambda e: page.go("/settings")),
            IconButton(icons.LOGOUT, tooltip="Выход", on_click=lambda e: page.go("/logout")),
        ],
    )

    # Добавляем AppBar в контролы страницы
    page.controls.append(app_bar)
