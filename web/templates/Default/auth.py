import time
from datetime import datetime

from flet import *

from urllib.parse import urlparse, parse_qs

from services.DatabaseService import JSONService
db_service = JSONService()


def extract_query_params(page: Page):
    # Извлечение URL из page.route
    url = page.route

    # Разбор URL для получения query string
    parsed_url = urlparse(url)

    # Извлечение query параметров в виде словаря
    query_params = parse_qs(parsed_url.query)

    # Преобразуем список значений для каждого ключа в простые строки
    query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

    return query_params

def tpl_auth(page: Page):
    page.title = 'Авторизация'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    query_params = extract_query_params(page)
    # Процесс ринг
    process_bar = ProgressBar(value=0)


    if db_service.find_one('users', {'tgid' : int(query_params.get('tgid'))}):
        user_data = db_service.find_one('users', {'tgid' : int(query_params.get('tgid'))})

        page.session.set('id', user_data.get('id'))
        page.session.set('tgid', user_data.get('tgid'))
        page.session.set('uname', user_data.get('username'))
        page.session.set('fname', user_data.get('fname'))
        page.session.set('lname', user_data.get('lname'))
        page.session.set('user_group', user_data.get('user_group'))
        page.session.set('is_premium', user_data.get('is_premium'))

        print(f'user group : {page.session.get('user_group')}')

        page.go('/settings/')


    form = Column(
        controls=[
            process_bar
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=10
    )

    return Stack(
        controls=[
            Column(
                expand_loose=True,
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        padding=20,
                        alignment=alignment.center,
                        margin=margin.symmetric(vertical=250),
                        content=form
                    )
                ]
            )
        ]
    )