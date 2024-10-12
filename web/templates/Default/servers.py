from flet import *

from web.templates.Default.auth import db_service


def tpl_servers(page: Page):
    # Настройка страницы
    page.title = "Список серверов"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = MainAxisAlignment.CENTER

    # Заголовок страницы
    header = Text("Серверы сообщества", size=20, text_align="left")

    # Получаем список серверов из базы данных
    servers = db_service.find_all('minecraft_servers', {'tgid': int(page.session.get('tgid'))})

    # Плавающая кнопка для добавления сервера
    add_server = FloatingActionButton(
        text="+",
        on_click=lambda _e: page.go('/add_server/'),
        bgcolor=colors.PRIMARY,
        tooltip="Добавить сервер",
        enable_feedback=True
    )

    # Формируем список карточек для серверов
    server_cards = []

    for server in servers:
        # Каждая карточка содержит название сервера, IP, порт и кнопку "глаз"
        server_card = Container(
            padding=10,
            border_radius=8,
            margin=margin.only(bottom=10),
            content=Row(
                controls=[
                    Column(
                        controls=[
                            Text(f"Название: {server.get('server_name')}", size=14),
                            Text(f"IP: {server.get('server_ip')}:{server.get('server_port')}", size=12),
                        ],
                        expand=True
                    ),
                    IconButton(
                        icon=icons.REMOVE_RED_EYE,
                        tooltip="Просмотр",
                        on_click=lambda e, server=server: view_server(server)  # Передаем информацию о сервере
                    ),
                    IconButton(
                        icon=icons.DELETE,
                        tooltip="Удалить",
                        on_click=lambda e, server_id=server.get('id'): delete_server(server_id)
                    )
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER
            )
        )
        server_cards.append(server_card)

    # Обработчик для просмотра сервера
    def view_server(server):
        bottom_sheet_content = Column(
            controls=[
                Text(f"Название сервера: {server.get('server_name')}", size=16),
                Text(f"IP: {server.get('server_ip')}:{server.get('server_port')}", size=14),
                Text(f"Версия: {server.get('version')}", size=14),
                Text(f"Игроков онлайн: {server.get('players_online')}", size=14),
            ],
            spacing=10,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.START
        )

        # Создание BottomSheet
        page.bottom_sheet = BottomSheet(
            content=Container(
                padding=20,
                content=bottom_sheet_content
            ),
            open=True  # Открываем BottomSheet сразу
        )
        page.update()

    # Обработчик для удаления сервера
    def delete_server(server_id):
        db_service.delete('minecraft_servers', server_id)
        page.snack_bar = SnackBar(content=Text("Сервер удален"), open=True)
        page.update()
        page.update()

    # Купертино-бар внизу
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

    # Основной контейнер с прокруткой и фиксированной нижней панелью
    return Column(
        controls=[
            Container(
                expand=True,
                content=Column(
                    scroll=ScrollMode.AUTO,
                    controls=[
                        header,
                        Column(
                            controls=server_cards,
                            spacing=10
                        )
                    ],
                    alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=25,
                )
            ),
            Container(
                alignment=alignment.bottom_right,
                content=add_server
            ),
            Container(
                height=60,
                padding=10,
                border_radius=10,
                bgcolor=colors.ON_SECONDARY,
                alignment=alignment.bottom_center,
                content=cupertino_bar
            )
        ],
        expand=True
    )
