from flet import *


def tpl_admin(page: Page):
    page.add(CupertinoFilledButton("Чат", on_click=lambda e: page.go("/chat")))
