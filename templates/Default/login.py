from flet import *
from flet_core.alignment import center
from flet_core.cupertino_icons import BOLD_UNDERLINE

import time

from services.DatabaseService import JSONService


def tpl_login(page: Page):
    page.title = 'Авторизация'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    if page.session.get('role') == 'user' or page.client_storage.get('role') == 'user':
        page.go('/index')

    user_login_input = TextField(label='Login')
    user_password_input = TextField(label='Password', password=True)
    check_remember = Checkbox(label='Remember me')

    def err_snack(e, err_text):
        page.snack_bar = SnackBar(content=Text(f'{err_text}', weight=BOLD_UNDERLINE))
        page.snack_bar.bgcolor = colors.RED
        page.snack_bar.open = True
        page.update()

    def success_snack(e, msg_text):
        page.snack_bar = SnackBar(content=Text(f'{msg_text}', weight=BOLD_UNDERLINE))
        page.snack_bar.bgcolor = colors.GREEN
        page.snack_bar.open = True
        page.update()

    def validate_form(e):
        if not user_login_input.value or not user_password_input.value:
            err_snack(e,  'Заполните все поля!')
        else:
            db_service = JSONService()
            user_data = db_service.find_one('users', {'login': user_login_input.value})
            login = user_data.get('login')
            psqd = user_data.get('password')
            if  login == user_login_input.value and psqd == user_password_input.value:
                success_snack(e, 'Вы успешно авторизовались!')
                page.session.set('login', user_data.get('login'))
                page.session.set('email', user_data.get('email'))
                page.session.set('role', user_data.get('role'))
                page.session.set('password', user_data.get('password'))
                page.go('/index')
                if check_remember.value:
                    page.client_storage.set('login', user_data.get('login'))
                    page.client_storage.set('email', user_data.get('email'))
                    page.client_storage.set('role', user_data.get('role'))
                    page.client_storage.set('route', f'{page.route}')
                    page.go('/index')


    submit_button = CupertinoFilledButton('Войти', on_click=validate_form, alignment=center)

    page.add(
        Container(
            # border= border.all(color=colors.GREY_100),
            border_radius=5,
            margin=10,
            bgcolor=colors.ON_SECONDARY,
            width=350,
            content=Column(
                [
                    Row(
                        [
                            Column(
                                [
                                    Container(
                                        bgcolor=colors.PRIMARY,
                                        width=350,
                                        padding=10,
                                        content=Text(page.title, color=colors.ON_PRIMARY, size=25),
                                    ),
                                    Container(
                                        padding=25,
                                        content=Column(
                                            [
                                                user_login_input,
                                                user_password_input,
                                                check_remember,
                                                submit_button
                                            ],
                                        )
                                    )
                                ],
                            )
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    )
                ]
            )
        )
    )
    page.update()