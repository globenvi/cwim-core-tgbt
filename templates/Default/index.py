from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    page.add(
        Container(
            # border=border.all(color=colors.GREY_100),
            border_radius=5,
            margin=10,
            padding=10,
            bgcolor=colors.ON_SECONDARY,
        )
    )

