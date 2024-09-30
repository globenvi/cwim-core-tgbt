from attr.setters import validate
from flet import *
from flet_core.alignment import center
from flet_core.cupertino_icons import BOLD_UNDERLINE


def main(page: Page):
    page.title = 'Авторизация'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER


    user_login_input = TextField(label='Login')
    user_password_input = TextField(label='Password', password=True)
    check_remember = Checkbox(label='Remember me')

    def err_snack(e):
        page.snack_bar = SnackBar(content=Text('Заполните все поля!', weight=BOLD_UNDERLINE))
        page.snack_bar.bgcolor = colors.RED
        page.snack_bar.open = True
        page.update()

    def validate_form(e):
        if not user_login_input.value or not user_password_input.value:
            err_snack(e)


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