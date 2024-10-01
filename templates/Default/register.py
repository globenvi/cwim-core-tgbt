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
        pb.visible = True
        page.update()

        if not db_service.find_one('users', {'login': user_login_input.value}):
            db_service.create('users', {
                'login': user_login_input.value,
                'password': user_password_input.value,
                'email': user_email_input.value,
                'user_group': 'user',
                'registration_date': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            pb.value = 100
            page.go('/login')

    async def validate_form(e):
        if not user_login_input.value or not user_password_input.value or not user_email_input.value:
            err_snack(e, 'Заполните все поля!')
        else:
            pb.visible = True
            page.update()
            await collect_data()
            success_snack(e, 'Регистрация прошла успешно!')

    submit_button = CupertinoFilledButton('Зарегистрироваться', on_click=validate_form, alignment=center)

    return Column(
        controls=[
            Text(page.title, size=25, weight="bold"),
            user_login_input,
            user_password_input,
            user_email_input,
            pb,
            submit_button
        ],
        alignment=MainAxisAlignment.CENTER
    )
