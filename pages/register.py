from flet import *
from rich.text import TextType


# Шаблон страницы регистрации
def tpl_register(page: Page):
    page.title = 'Sign Up'
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.theme_mode = ThemeMode.SYSTEM

    page.add(Text('register page'))
