from flet import *

def tpl_index(page: Page):
    page.title = "Home Page"
    page.vertical_alignment = "start"

    header = AppBar(
        title=Text("Home"),
        bgcolor="#1976D2",
        color="#FFFFFF"
    )

    rail = NavigationRail(
        selected_index=0,
        label_type=NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=FloatingActionButton(icon=icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.HOME, selected_icon=icons.HOME, label="Home"
            ),
            NavigationRailDestination(
                icon=icons.PERSON, selected_icon=icons.PERSON, label="Profile"
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED, selected_icon=icons.SETTINGS, label="Settings"
            ),
            NavigationRailDestination(
                icon=icons.LOGOUT, selected_icon=icons.LOGOUT, label="Logout"
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
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
