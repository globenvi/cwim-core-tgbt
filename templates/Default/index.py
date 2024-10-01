from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM

    page.appbar = AppBar(
        leading=icons.GITE,
        leading_width=40,
        title=Text(page.title),
        bgcolor=colors.ON_PRIMARY,
        actions=[]
    )

