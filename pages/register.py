from flet import *
from rich.text import TextType


# Шаблон страницы регистрации
def tpl_register(page: Page):
    page.title = 'Sign Up'
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.theme_mode = ThemeMode.SYSTEM

    text_username: TextField = TextField(label='Username', text_align=TextAlign.LEFT, width=200, on_change=validate)
    text_password: TextField = TextField(label='Password', text_align=TextAlign.LEFT, width=200, password=True, on_change=validate)
    checkbox_signup: Checkbox = Checkbox(label='I agree to the Terms and Conditions', value=False)
    button_submit: ElevatedButton = ElevatedButton(text='Sign Up', disabled=True)

    def validate(e: ControlEvent):
        if all([text_password.value, text_username.value, checkbox_signup.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True

        page.update()

    page.add(
        Row(
            controls=[
                Column(
                    [
                        text_username,
                        text_password,
                        checkbox_signup,
                        button_submit,
                    ]
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )
