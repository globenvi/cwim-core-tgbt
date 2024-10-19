from flet import *


cupertino_bar = Row(
    controls=[

        IconButton(icon=icons.SETTINGS, tooltip="Настройки", on_click=lambda e: page.go('/settings/'), bgcolor=colors.PRIMARY, icon_color=colors.ON_PRIMARY),
        IconButton(icon=icons.MESSENGER, tooltip="Чат", on_click=lambda e: page.go('/chat/')),
        IconButton(icon=icons.PERSON_4, tooltip="Профиль", on_click=lambda e: page.go('/profile/')),
        IconButton(icon=icons.BROWSER_UPDATED, tooltip="Мои сервера", visible=True, on_click=lambda e: page.go('/servers/')),
    ],
    alignment=MainAxisAlignment.CENTER,
    spacing=10,
)