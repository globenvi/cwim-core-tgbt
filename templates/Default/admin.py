from flet import Column, Text, ElevatedButton, Container

def tpl_admin(page):
    # Контент админ-панели
    content = Container(
        content=Column(
            controls=[
                Text("Админ-панель", size=20, weight="bold"),
                ElevatedButton("Управление пользователями", on_click=lambda e: page.go("/users")),
                ElevatedButton("Настройки системы", on_click=lambda e: page.go("/settings")),
            ],
            alignment="center"
        ),
        alignment="center",
        width=300,
        padding=10,
    )
    page.controls.append(content)
    page.update()
