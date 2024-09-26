from flet import Column, TextField, ElevatedButton, Text, Container

def tpl_register(page):
    # Контейнер с формой регистрации
    form = Container(
        content=Column(
            controls=[
                Text("Регистрация", size=20, weight="bold"),
                TextField(label="Имя пользователя"),
                TextField(label="Email"),
                TextField(label="Пароль", password=True),
                ElevatedButton("Зарегистрироваться", on_click=lambda e: page.go("/index")),
            ],
            alignment="center"
        ),
        alignment="center",
        width=300,
        padding=10,
    )
    page.controls.append(form)
    page.update()
