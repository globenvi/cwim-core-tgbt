import flet as ft

def main(page: ft.Page):
    page.title = "Admin Panel"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Заголовок
    header = ft.Row(
        [
            ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS, size=40),
            ft.Text("Admin Panel", size=30, weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Меню навигации
    nav_menu = ft.Column(
        [
            ft.ListTile(title=ft.Text("Dashboard")),
            ft.ListTile(title=ft.Text("Users")),
            ft.ListTile(title=ft.Text("Settings")),
            ft.ListTile(title=ft.Text("Logs")),
        ],
        spacing=10,
    )

    # Основной контент
    content_area = ft.Column(
        [
            ft.Text("Welcome to the Admin Panel!", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Here you can manage your application.", size=18),
            ft.Divider(),
            ft.Row(
                [
                    ft.Card(
                        content=ft.Column(
                            [
                                ft.Text("Total Users", size=18),
                                ft.Text("120", size=36, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        elevation=2,
                        width=150,
                    ),
                    ft.Card(
                        content=ft.Column(
                            [
                                ft.Text("Active Sessions", size=18),
                                ft.Text("45", size=36, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        elevation=2,
                        width=150,
                    ),
                    ft.Card(
                        content=ft.Column(
                            [
                                ft.Text("Pending Tasks", size=18),
                                ft.Text("7", size=36, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        elevation=2,
                        width=150,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Основной макет
    page.add(
        ft.Column(
            [
                header,
                ft.Row(
                    [
                        ft.Container(
                            nav_menu,
                            width=200,
                            bgcolor=ft.colors.BLUE_GREY_50,
                        ),
                        ft.VerticalDivider(),
                        ft.Expanded(content=content_area),
                    ]
                ),
            ]
        )
    )
