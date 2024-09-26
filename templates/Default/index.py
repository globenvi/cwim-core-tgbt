from flet import Column, Text, Container

def tpl_index(page):
    # Контент главной страницы
    content = Container(
        content=Column(
            controls=[
                Text("Добро пожаловать на главную страницу", size=20, weight="bold"),
            ],
            alignment="center"
        ),
        alignment="center",
        width=300,
        padding=10,
    )
    page.controls.append(content)
    page.update()
