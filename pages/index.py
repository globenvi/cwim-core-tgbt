from flet import *

def tpl_index(page: Page):
    page.title = "Главная"
    page.add(Text("Это главная страница"))
    page.update()
