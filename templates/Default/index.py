from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM

    page.horizontal_alignment = page.vertical_alignment = "center"

    page.floating_action_button = FloatingActionButton(icon=icons.ADD)
    page.floating_action_button_location = FloatingActionButtonLocation.CENTER_DOCKED

    page.appbar = AppBar(
        title=Text("Bottom AppBar Demo"),
        center_title=True,
        bgcolor=colors.GREEN_300,
        automatically_imply_leading=False,
    )
    page.bottom_appbar = BottomAppBar(
        bgcolor=colors.BLUE,
        shape=NotchShape.CIRCULAR,
        content=Row(
            controls=[
                IconButton(icon=icons.MENU, icon_color=colors.WHITE),
                Container(expand=True),
                IconButton(icon=icons.SEARCH, icon_color=colors.WHITE),
                IconButton(icon=icons.FAVORITE, icon_color=colors.WHITE),
            ]
        ),
    )

    page.add(Text("Body!"))
    user_data = page.client_storage.get('role')
