import flet as ft

def main(page: ft.Page):
    # Установка заголовка страницы
    page.title = "Login Page"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE

    # Заголовок
    title = ft.Text(
        "Welcome Back!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE,
        text_align=ft.TextAlign.CENTER,
        padding=ft.padding.only(top=20, bottom=20)
    )

    # Поля для ввода
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, width=300)

    # Функция обработки нажатия кнопки входа
    def on_login_click(e):
        if username.value == "admin" and password.value == "password":  # Пример проверки
            page.add(ft.Text("Login successful!", color=ft.colors.GREEN))
        else:
            page.add(ft.Text("Invalid credentials", color=ft.colors.RED))

    # Кнопка входа
    login_button = ft.ElevatedButton("Login", on_click=on_login_click, width=300)

    # Создаем контейнер для формы
    form_container = ft.Column(
        controls=[
            username,
            password,
            login_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # Основной контейнер для страницы
    main_container = ft.Column(
        controls=[
            title,
            form_container
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.add(main_container)