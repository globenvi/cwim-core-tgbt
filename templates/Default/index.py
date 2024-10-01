from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM

    page.add(
        Text('WELCOME TO HOME PAGE')
    )
