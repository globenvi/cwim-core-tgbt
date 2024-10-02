from tkinter import Button

from flet import *

def tpl_login(page: Page):
    page.title = 'Авторизация'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Заголовок формы
    from_header = Text('Авторизация', size=25, text_align=alignment.center)

    # Поля ввода
    user_login_input = TextField(label='Логин', expand=True)
    user_password_input = TextField(label='Пароль', expand=True, password=True, can_reveal_password=True)
    user_remember_switch = CupertinoSwitch(label="Запомнить?")
    user_redirect_register_button = TextButton(text='Нет аккаунта?', on_click=lambda _e: page.go("/register"))
    user_data_submit_button = CupertinoFilledButton(text='Войти', icon=icons.LOGIN)

    # Определение формы
    form = Column(
        controls=[
            from_header,
            user_login_input,
            user_password_input,
            user_remember_switch,
            user_redirect_register_button,
            user_data_submit_button
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