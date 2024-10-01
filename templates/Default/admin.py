import flet as ft

def tpl_admin(page: ft.Page):
    page.title = "Admin Panel"
    page.vertical_alignment = "start"

    # Header
    header = ft.AppBar(
        title=ft.Text("Admin Panel"),
        bgcolor="#1976D2",
        color="#FFFFFF"
    )

    # Sidebar (Navigation Rail)
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.DASHBOARD, selected_icon=ft.icons.DASHBOARD, label="Dashboard"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PERSON, selected_icon=ft.icons.PERSON, label="Users"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED, selected_icon=ft.icons.SETTINGS, label="Settings"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOGOUT, selected_icon=ft.icons.LOGOUT, label="Logout"
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    # Content area
    content = ft.Column(
        controls=[
            ft.Text("Welcome to the Admin Panel!", size=24),
            ft.Text("Here you can manage users and settings.", size=16),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=True,
        expand=True,
    )

    # Footer
    footer = ft.Container(
        content=ft.Text("© 2024 Admin Panel"),
        padding=10,
        alignment=ft.alignment.center
    )

    # Adding components to the page
    page.add(
        header,
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content,
            ],
            expand=True,
        ),
        footer
    )