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
                    expand=True,
                )
            ]
        ),
        Row(
            [
                Container(
                    border_radius=5,
                    bgcolor=colors.BLUE,
                    width=300,
                    height=300,
                    padding=20,
                ),
                Container(
                    border_radius=5,
                    bgcolor=colors.BLUE,
                    height=300,
                    padding=20,
                    expand=True,
                )
            ]
        ),
        Row(
            [
                Container(
                    border_radius=5,
                    bgcolor=colors.GREEN,
                    padding=20,
                    expand=True,
                    bottom=0
                )
            ],
        )
    )
