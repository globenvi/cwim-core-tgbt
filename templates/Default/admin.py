import flet as ft
import random
from datetime import datetime, timedelta

class User:
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.online = random.choice([True, False])
        self.last_login = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")

class Post:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author
        self.date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")

class Comment:
    def __init__(self, id, content, author):
        self.id = id
        self.content = content
        self.author = author
        self.date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")

def tpl_admin(page: ft.Page):
    page.title = "Admin Panel"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)

    # Data storage
    users = [User(i, f"User {i}", f"user{i}@example.com", random.choice(["Admin", "User", "Moderator"])) for i in range(1, 101)]
    posts = [Post(i, f"Post {i}", f"User {random.randint(1, 100)}") for i in range(1, 51)]
    comments = [Comment(i, f"Comment {i}", f"User {random.randint(1, 100)}") for i in range(1, 101)]

    def save_data(data_type, item):
        if data_type == "users":
            users.append(item)
        elif data_type == "posts":
            posts.append(item)
        elif data_type == "comments":
            comments.append(item)
        page.update()

    # Color palettes
    color_palettes = {
        "Blue": ft.colors.BLUE,
        "Red": ft.colors.RED,
        "Green": ft.colors.GREEN,
        "Purple": ft.colors.PURPLE,
        "Orange": ft.colors.ORANGE,
        "Teal": ft.colors.TEAL,
        "Pink": ft.colors.PINK,
        "Indigo": ft.colors.INDIGO,
        "Cyan": ft.colors.CYAN,
        "Amber": ft.colors.AMBER,
    }

    # Drawer
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Admin Panel", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.DASHBOARD),
                        title=ft.Text("Dashboard"),
                        on_click=lambda _: update_content(0)
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PEOPLE),
                        title=ft.Text("Users"),
                        on_click=lambda _: update_content(1)
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SETTINGS),
                        title=ft.Text("Settings"),
                        on_click=lambda _: update_content(2)
                    ),
                ]),
                padding=10
            )
        ],
    )

    def toggle_drawer():
        page.drawer.open = not page.drawer.open
        page.update()

    # Custom Header
    def create_header():
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(ft.icons.MENU, on_click=lambda _: toggle_drawer()),
                    ft.Text("Admin Panel", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.TextButton("Go to Main", on_click=lambda _: print("Go to Main clicked")),
                    ft.TextButton("Log out", on_click=lambda _: print("Log out clicked")),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

    # Content
    content = ft.Container(padding=20)

    def create_chart():
        chart_data = [random.randint(10, 100) for _ in range(7)]
        return ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[ft.BarChartRod(from_y=0, to_y=value, width=20, color=ft.colors.BLUE)],
                )
                for i, value in enumerate(chart_data)
            ],
            left_axis=ft.ChartAxis(labels_size=40),
            bottom_axis=ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=i, label=ft.Text(f"Day {i+1}")) for i in range(7)]
            ),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_300, width=1),
            max_y=100,
            expand=True,
        )

    def create_data_table(data, columns, rows_per_page=10):
        return ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in columns],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(getattr(item, col.lower())))) for col in columns])
                for item in data[:rows_per_page]
            ],
        )

    def create_dashboard():
        return ft.Column([
            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Total Users", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(str(len(users)), size=40),
                        ]),
                        padding=20,
                    ),
                    width=200,
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Online Users", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(str(sum(1 for user in users if user.online)), size=40),
                        ]),
                        padding=20,
                    ),
                    width=200,
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Today's Users", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(str(sum(1 for user in users if user.last_login == datetime.now().strftime("%Y-%m-%d"))), size=40),
                        ]),
                        padding=20,
                    ),
                    width=200,
                ),
            ]),
            ft.Container(height=20),
            ft.Text("Recent Posts", size=20, weight=ft.FontWeight.BOLD),
            create_data_table(posts[:5], ["ID", "Title", "Author", "Date"]),
            ft.Container(height=20),
            ft.Text("Recent Comments", size=20, weight=ft.FontWeight.BOLD),
            create_data_table(comments[:5], ["ID", "Content", "Author", "Date"]),
        ])

    def create_users_view():
        return ft.Column([
            ft.Text("Users", size=32, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=create_data_table(users, ["ID", "Name", "Email", "Role"]),
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=5,
                padding=10,
            ),
            ft.Row([
                ft.ElevatedButton("Previous", on_click=lambda _: print("Previous clicked")),
                ft.ElevatedButton("Next", on_click=lambda _: print("Next clicked")),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ])

    def create_settings_view():
        def change_theme(e):
            page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            page.update()

        def change_color_scheme(e):
            page.theme = ft.Theme(color_scheme_seed=color_palettes[e.control.value])
            page.update()

        return ft.Column([
            ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Text("Theme", size=20, weight=ft.FontWeight.BOLD),
            ft.Switch(label="Dark mode", on_change=change_theme),
            ft.Container(height=20),
            ft.Text("Color Scheme", size=20, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                options=[ft.dropdown.Option(color) for color in color_palettes.keys()],
                width=200,
                on_change=change_color_scheme,
            ),
        ])

    def update_content(index):
        content.content = (
            create_dashboard() if index == 0 else
            create_users_view() if index == 1 else
            create_settings_view() if index == 2 else
            ft.Text("Unknown page")
        )
        page.drawer.open = False
        page.update()

    # Layout
    def layout_page():
        return ft.Column([
            create_header(),
            content
        ], expand=True)

    page.drawer = drawer
    update_content(0)
    return layout_page()

