from urllib.parse import urlparse, parse_qs
from flet import *

from services.DatabaseService import JSONService
from core.controllers.UserController import User

db_service = JSONService()

def extract_query_params(page: Page):
    # Извлечение URL из page.route
    url = page.route
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
    return query_params

async def tpl_profile(page: Page):
    # Настройка страницы
    page.title = "Настройки"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    tgid = extract_query_params(page).get('tgid')


    # Основной контейнер с прокруткой и фиксированной нижней панелью
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
                            # content=Text,
                            alignment=alignment.center
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=25,
                )
            ),
        ],
        expand=True  # Позволяем контейнеру занимать всю доступную высоту
    )
