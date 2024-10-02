from flet import *

from services.DatabaseService import JSONService
db_service = JSONService()

def tpl_login(page: Page):
    page.title = 'Авторизация'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Заголовок формы
    from_header = Text('Авторизация', size=25, text_align=alignment.center)

    # Процесс бар
    process_bar = ProgressBar(visible=False)

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

    def validation_form(e):
        process_bar.visible = True
        page.update()

        user_data = db_service.find_one('users', {'login': user_login_input.value})

        if user_data:
            if user_data.get('password') == user_password_input.value and user_data.get('login') == user_login_input.value:
                page.session.set('id', user_data.get('id'))
                page.session.set('login', user_data.get('login'))
                page.session.set('email', user_data.get('email'))
                page.session.set('role', user_data.get('role'))
                page.session.set('registered_date', user_data.get('registered_date'))
                success_snack('Авторизация прошла успешно!')
                process_bar.visible = False
                page.update()

                if user_remember_switch.value:
                    page.client_storage.set('id', user_data.get('id'))
                    page.client_storage.set('login', user_data.get('login'))
                    page.client_storage.set('email', user_data.get('email'))
                    page.client_storage.set('role', user_data.get('role'))
                    page.client_storage.set('registered_date', user_data.get('registered_date'))
                    page.go('/index')
                page.go('/index')
            else:
                process_bar.visible = False
                page.update()
                error_snack('Неверный логин или пароль!')

    # Поля ввода
    user_login_input = TextField(label='Логин', expand=True)
    user_password_input = TextField(label='Пароль', expand=True, password=True, can_reveal_password=True)
    user_remember_switch = CupertinoSwitch(label="Запомнить?")
    user_redirect_register_button = TextButton(text='Нет аккаунта?', on_click=lambda _e: page.go("/register"))
    user_data_submit_button = CupertinoFilledButton(text='Войти', icon=icons.LOGIN, on_click=validation_form)

    # Определение формы
    form = Column(
        controls=[
            from_header,
            user_login_input,
            user_password_input,
            user_remember_switch,
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
                  height=350,
                  content=form
              )
          )
        ],
    )