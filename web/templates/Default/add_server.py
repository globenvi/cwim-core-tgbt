import time
from flet import *

from web.templates.Default.auth import db_service


def tpl_add_server(page: Page):
    # Настройка страницы
    page.title = "Добавить сервер"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = MainAxisAlignment.CENTER

    # Заголовок страницы
    header = Text("Добавить новый сервер", size=20, text_align="left")

    # Поля ввода информации о сервере
    server_name_input = TextField(label="Название сервера", expand=True)
    server_ip_input = TextField(label="IP-адрес сервера", expand=True)
    server_port_input = TextField(label="Порт сервера", expand=True, value="19132")  # По умолчанию порт Bedrock Edition

    # Кнопка сохранения
    save_button = CupertinoFilledButton(text="Добавить сервер", icon=icons.SAVE, on_click=lambda e: save_server())

    # Обработчик сохранения сервера
    def save_server():
        db_service.create('minecraft_servers', {
            "tgid": page.session.get('tgid'),  # Привязываем сервер к пользователю
            "server_name": server_name_input.value,
            "server_ip": server_ip_input.value,
            "server_port": server_port_input.value
        })
        page.snack_bar = SnackBar(content=Text("Сервер успешно добавлен"), open=True)
        page.update()
        time.sleep(3)
        page.go('/servers/')

    # Основное содержимое страницы (форма добавления сервера)
    add_server_column = Column(
        controls=[
            header,
            server_name_input,
            server_ip_input,
            server_port_input,
            save_button
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # Нижняя панель (Купертино-бар)
    cupertino_bar = Row(
        controls=[
            IconButton(icon=icons.SETTINGS, tooltip="Настройки", on_click=lambda e: page.go('/settings/')),
            IconButton(icon=icons.MESSENGER, tooltip="Чат", on_click=lambda e: page.go('/chat/')),
            IconButton(icon=icons.PERSON_4, tooltip="Профиль", on_click=lambda e: page.go('/profile/')),
            IconButton(icon=icons.BROWSER_UPDATED, tooltip="Мои сервера", visible=True, on_click=lambda e: page.go('/servers/')),
        ],
        alignment=MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Основной макет страницы с зафиксированной нижней панелью и прокручиваемым содержимым
    return Column(
        controls=[
            Container(
                expand=True,
                content=Column(
                    scroll=ScrollMode.AUTO,
                    controls=[
                        Container(
                            bgcolor=colors.ON_SECONDARY,
                            padding=20,
                            margin=10,
                            border_radius=10,
                            content=add_server_column,
                            alignment=alignment.center
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=25,
                )
            ),
            Container(
                height=60,
                padding=10,
                bgcolor=colors.ON_SECONDARY,
                alignment=alignment.bottom_center,
                content=cupertino_bar,
            )
        ],
        expand=True
    )
