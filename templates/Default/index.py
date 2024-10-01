from flet import *

def main(page: Page):
    # Флаг для отслеживания состояния меню
    menu_open = Ref[bool](True)

    # Функция для переключения состояния меню
    def toggle_menu(e):
        menu_open.value = not menu_open.value
        page.update()

    # Определение выдвижного меню
    menu = NavigationRail(
        selected_index=0,
        label_type=NavigationRailLabelType.ALL,
        min_width=100,
        leading=FloatingActionButton(
            icon=icons.MENU,
            text="Menu",
            on_click=toggle_menu,
        ),
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.FAVORITE_BORDER,
                selected_icon=icons.FAVORITE,
                label="Index",
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.BOOKMARK_BORDER),
                selected_icon_content=Icon(icons.BOOKMARK),
                label="Profile",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon_content=Icon(icons.SETTINGS),
                label_content=Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    # Добавляем контент страницы
    content = Column([
        Text("Welcome to the Home Page!", size=30),
        Text("Here you can find various functionalities."),
        Text("Use the navigation menu to switch between pages."),
    ])

    # Основная структура страницы
    page.add(
        Row(
            [
                Column(
                    [
                        menu if menu_open.value else Container(),
                        VerticalDivider(width=1),
                        content,
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

    content = Column(
        controls=[
            Text("Welcome to the Home Page!", size=24),
            Text("Here is some important information.", size=16),
        ],
        alignment=MainAxisAlignment.CENTER,
        scroll=True,
        expand=True,
    )

    footer = Container(
        content=Text("© 2024 Home Page"),
        padding=10,
        alignment=alignment.center
    )

    page.add(
        header,
        Row(
            [
                rail,
                VerticalDivider(width=1),
                content,
            ],
            expand=True,
        ),
        footer
    )
