from flet import *


def tpl_admin(page: Page):
    page.title = "Админ центр"
    page.theme_mode = ThemeMode.SYSTEM
    page.add(Text("Страница админ-панели"))
    page.update()