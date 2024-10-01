# admin.py
from flet import Page, AppBar, Column, Text, Row, Container, IconButton, icons, NavigationRail

def tpl_admin(page: Page):
    page.title = "Admin Panel"
    page.vertical_alignment = "start"

    # Header
    header = AppBar(
        title=Text("Admin Panel"),
        bgcolor="#1976D2",
        color="#FFFFFF"
    )

    # Side Menu (Navigation Rail)
    side_menu = NavigationRail(
        extended=True,
        destinations=[
            icons.NavigationRailDestination(icon=icons.DASHBOARD, label="Dashboard"),
            icons.NavigationRailDestination(icon=icons.SETTINGS, label="Settings"),
            icons.NavigationRailDestination(icon=icons.PERSON, label="Profile"),
            icons.NavigationRailDestination(icon=icons.LOGOUT, label="Logout"),
        ],
        selected_index=0,  # Начальный индекс выбранного пункта
    )

    # Content area
    content = Column(
        controls=[
            Text("Welcome to the Admin Panel!", size=24),
            Text("Here you can manage users and settings.", size=16),
        ],
        alignment="center",
        scroll=True,
    )

    # Footer
    footer = Container(
        content=Text("© 2024 Admin Panel"),
        padding=10,
        alignment="center"
    )

    # Добавляем компоненты на страницу
    page.add(header, Row([side_menu, content]), footer)
