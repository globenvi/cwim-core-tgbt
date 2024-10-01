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

    if page.session.get('user_group') == 'user' or page.client_storage.get('user_group') == 'user':
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
            if user_data and user_data.get('password') == user_password_input.value:
                success_snack(e, 'Вы успешно авторизовались!')
                # Установить значения в сессии
                page.session.set('id', user_data.get('id'))
                page.session.set('user_group', user_data.get('user_group'))
                page.session.set('login', user_data.get('login'))
                page.session.set('email',  user_data.get('email'))
                page.session.set('telegram_id', user_data.get('telegram_id'))
                if page.session.get('user_group') != 'guest':
                    page.go('/index')
            else:
                err_snack(e, 'Пользователь не найден или неверный логин/пароль!')

    submit_button = CupertinoFilledButton('Войти', on_click=validate_form, alignment=center)

    return Column(
        controls=[
            Text(page.title, size=25, weight="bold"),
            user_login_input,
            user_password_input,
            check_remember,
            submit_button
        ],
        alignment=MainAxisAlignment.CENTER
    )
