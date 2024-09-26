from flet import Column, TextField, ElevatedButton, Text, Container

def tpl_login(page):
    # Контейнер с формой входа
    form = Container(
        content=Column(
            controls=[
                Text("Авторизация", size=20, weight="bold"),
                TextField(label="Имя пользователя"),
                TextField(label="Пароль", password=True),
                ElevatedButton("Войти", on_click=lambda e: page.go("/index")),
            ],
            alignment="center"
        ),
        alignment="center",
        width=300,
        padding=10,
    )
    page.controls.append(form)
    page.update()
