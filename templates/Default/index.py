from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM
    page.vertical_alignment = VerticalAlignment.CENTER

    page.add(
        Row(
            [
                Container(
                    border_radius=5,
                    bgcolor=colors.RED,
                    padding=20,
                    margin=20,
                    rtl=True,
                )
            ]
        )
    )
