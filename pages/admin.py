from flet import *


def tpl_admin(page: Page):
    import flet as ft

    def main(page: ft.Page):
        page.title = "Сайдбар с анимацией"

        # Функция для показа/скрытия сайдбара
        def toggle_sidebar(e):
            if sidebar_container.width == 0:
                sidebar_container.width = 200  # Устанавливаем ширину при показе
            else:
                sidebar_container.width = 0  # Прячем сайдбар

            sidebar_container.update()

        # Создаём сайдбар
        sidebar_container = ft.Container(
            width=0,  # Начальная ширина скрытого сайдбара
            bgcolor=ft.colors.BLUE_GREY_900,
            content=ft.Column(
                [
                    ft.Text("Главная", color=ft.colors.WHITE),
                    ft.Text("Профиль", color=ft.colors.WHITE),
                    ft.Text("Настройки", color=ft.colors.WHITE),
                    ft.Text("Выход", color=ft.colors.WHITE),
                ],
                tight=True,
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=10,
            animate=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
        )

        # Кнопка для открытия/закрытия сайдбара
        toggle_button = ft.IconButton(
            icon=ft.icons.MENU,
            on_click=toggle_sidebar,
            tooltip="Открыть/Закрыть меню",
        )

        # Добавляем контент на страницу
        page.add(
            ft.Row(
                [
                    sidebar_container,  # Сайдбар
                    ft.Container(
                        content=ft.Text("Основной контент страницы"),
                        expand=True,
                        padding=20
                    )
                ],
                expand=True
            ),
            ft.FloatingActionButton(icon=ft.icons.MENU, on_click=toggle_sidebar),  # Плавающая кнопка
        )

