from flet import *
from flet_core.alignment import center
from flet_core.cupertino_icons import BOLD_UNDERLINE

from services.DatabaseService import JSONService


import time


def tpl_register(page: Page):
    page.title = 'Регистрация'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    if page.session.get('user_group') == 'user' or page.client_storage.get('user_group') == 'user':
        page.go('/index')

    user_login_input = TextField(label='Login')
    user_password_input = TextField(label='Password', password=True)
    user_email_input = TextField(label='Email')
    user_telegramid_input = TextField(label='Telegram ID', visible=False, password=True)

    pb = ProgressBar(width=300, value=0, visible=False)

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


    async def collect_data():
        db_service = JSONService()
        pb.value = 50

        if not db_service.find_one('users', {'login': user_login_input.value}):
            pb.value = 75
            db_service.create('users', {
                'login': user_login_input.value,
                'password': user_password_input.value,
                'email': user_email_input.value,
                'user_group': 'user',  # Значение по умолчанию
                'telegram_id': user_telegramid_input.value if user_telegramid_checkbox.value else None,
                'registration_date': time.strftime('%Y-%m-%d %H:%M:%S')})
            pb.value = 100
            page.go('/login')


    async def validate_form(e):
        if user_telegramid_checkbox.value:
            user_telegramid_input.visible = True
            page.update()
        else:
            user_telegramid_input.visible = False
            page.update()
        if not user_login_input.value or not user_password_input.value or not user_email_input.value:
            err_snack(e, 'Заполните все поля!')
        else:
            if len(user_login_input.value) < 6:
                err_snack(e, 'Логин должен быть не менее 6 символов!')
                return
            if user_email_input.value.find('@') == -1 or not user_email_input.value.endswith('.com') and not user_email_input.value.endswith('.ru'):
                err_snack(e, 'E-mail введен некорректно!')
                return
            if len(user_password_input.value) < 8:
                err_snack(e, 'Пароль должен быть не менее 8 символов!')
                return

            pb.visible = True
            page.update()
            pb.value = 10
            await collect_data()
            pb.value = 35
            success_snack(e, 'Регистрация прошла успешно!')


    async def telegramid_set(e):
        if user_telegramid_checkbox:
            user_telegramid_input.visible = True
            page.update()
        else:
            user_telegramid_input.visible = False
            page.update()

    user_telegramid_checkbox = CupertinoSwitch(label='Use TelegramID?', on_change=telegramid_set)
    user_data_submit_button = CupertinoFilledButton('Зарегистрироваться', on_click=validate_form, alignment=center)

    page.add(
        Container(
            # border= border.all(color=colors.GREY_100),
            border_radius=5,
            margin=10,
            bgcolor=colors.ON_SECONDARY,
            width=360,
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
                                                pb,
                                                user_login_input,
                                                user_password_input,
                                                user_email_input,
                                                user_telegramid_checkbox,
                                                user_telegramid_input,
                                                user_data_submit_button
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