import time
from datetime import datetime

from flet import *

from services.DatabaseService import JSONService
db_service = JSONService()

def tpl_register(page: Page):
    page.title = 'Авторизация'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    #SNACKS
    page.snack_bar = SnackBar(
        content=Text("Hello, world!"),
        action="Alright!",
    )

    def error_snack(message):
        page.snack_bar = SnackBar(Text(f'{message}'))
        page.snack_bar.bgcolor = colors.RED
        page.snack_bar.open = True
        page.update()

    def success_snack(message):
        page.snack_bar = SnackBar(Text(f'{message}'))
        page.snack_bar.bgcolor = colors.GREEN
        page.snack_bar.open = True
        page.update()

    # Заголовок формы
    from_header = Text('Регистрация', size=25, text_align=alignment.center)

    # Процесс ринг
    process_bar = ProgressBar(visible=False)

    # Validation
    async def validate_form_data(e):
        process_bar.visible = True
        page.update()

        user_data = db_service.find_one('users', {'login': user_login_input.value})

        if user_data:
            process_bar.visible = False
            page.update()
            error_snack('Пользователь с такими данными уже существует!')
            return

        if not user_login_input.value:
            process_bar.visible = False
            page.update()
            error_snack('Не указан логин!')
            return

        if not user_email_input.value.find('@') or not user_email_input.value.endswith('.com') and not user_email_input.value.endswith('.ru'):
            process_bar.visible = False
            page.update()
            error_snack('Не корректно указана почта')
            return

        if not user_password_input.value:
            process_bar.visible = False
            page.update()
            error_snack('Не указан пароль!')
            return

        if len(user_password_input.value) < 7:
            process_bar.visible = False
            page.update()
            error_snack('Минимальная длинна пароля 7 знаков!')
            return


        db_service.create('users', {
            'login': user_login_input.value,
            'email': user_email_input.value,
            'password': user_password_input.value,
            'role': "user",
            'registerd_date': datetime.now().isoformat(),
            'auth_method': 'default',
        })

        process_bar.visible = False
        success_snack('Добро пожаловать! Теперь авторизуйтесь.')
        page.go('/login')




    # Поля ввода
    user_login_input = TextField(label='Логин', expand=True)
    user_email_input = TextField(label='Почта', expand=True)
    user_password_input = TextField(label='Пароль', expand=True, password=True, can_reveal_password=True)
    user_redirect_register_button = TextButton(text='Есть аккаунт?', on_click=lambda _e: page.go("/login"))
    user_data_submit_button = CupertinoFilledButton(text='Зарегистрироваться', icon=icons.APP_REGISTRATION, on_click=validate_form_data)

    # Определение формы
    form = Column(
        controls=[
            from_header,
            user_login_input,
            user_email_input,
            user_password_input,
            user_redirect_register_button,
            Column(
                [
                    user_data_submit_button,
                    process_bar
                ]
            )
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=10
    )

    # Возврат главного контейнера
    return Column(
        [
          Container(
              padding=20,
              alignment=alignment.center,
              expand=True,
              content=Container(
                  bgcolor=colors.ON_SECONDARY,
                  border_radius=10,
                  padding=20,
                  alignment=alignment.center,
                  width=340,
                  height=360,
                  content=form
              )
          )
        ],
    )