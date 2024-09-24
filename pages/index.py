import json
import flet as ft

# Функция для загрузки конфигурации из config.json
def load_config():
    with open('./cwim-core-tgbt/config.json', 'r') as f:
        return json.load(f)

def tpl_index(page: ft.Page):
    page.title = "Админ центр - Авторизация"

    # Инициализация состояния темы (из сессии)
    if page.session.get("theme_mode") is None:
        page.session.set("theme_mode", ft.ThemeMode.LIGHT)  # По умолчанию светлая тема

    page.theme_mode = page.session.get("theme_mode")

    # Настройка центрального выравнивания содержимого страницы
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Загружаем пароль админа из конфигурации
    config = load_config()
    admin_password = config.get('admin_pass', '')

    # Поле для ввода пароля
    password_field = ft.TextField(
        label="Введите пароль:",
        password=True,
        can_reveal_password=True,
        width=300,
        text_align=ft.TextAlign.LEFT,
    )

    # Кнопка авторизации
    login_button = ft.CupertinoFilledButton(
        "Войти",
        on_click=lambda e: authenticate(password_field.value, admin_password, page),
        width=200
    )

    # Создание выпадающего списка для навигации
    dropdown = ft.Dropdown(
        label="Выберите страницу",
        hint_text="Перейдите на страницу",
        options=[
            ft.dropdown.Option("Главная"),
            ft.dropdown.Option("Чат"),
            ft.dropdown.Option("Админ панель"),
        ],
        on_change=lambda e: page.go(get_page_value(e.control.selected_option)),  # Переход на выбранную страницу
        autofocus=True,
    )

    # AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("Админ центр"),
        center_title=True,
        bgcolor=ft.colors.BLUE,
    )

    # BottomAppBar с выпадающим списком
    page.bottom_app_bar = ft.BottomAppBar(
        content=ft.Row(
            [
                dropdown
            ],
            alignment=ft.MainAxisAlignment.START,
        )
    )

    # Добавляем элементы на страницу
    page.add(
        ft.Column(
            [
                ft.Text(
                    "Авторизация",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                password_field,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    page.update()

def get_page_value(selected_option):
    """Возвращает значение страницы в зависимости от выбранного элемента."""
    if selected_option.text == "Главная":
        return "/"
    elif selected_option.text == "Чат":
        return "/chat"
    elif selected_option.text == "Админ панель":
        return "/admin"
    return "/"  # По умолчанию возвращаем главную страницу

def authenticate(input_password: str, admin_password: str, page: ft.Page):
    """Проверяет введенный пароль и управляет сессией."""
    if input_password == admin_password:
        # Пароль верный, авторизуем пользователя
        page.snack_bar = ft.SnackBar(ft.Text("Авторизация успешна!"), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.session.set("user_group", "admin")  # Устанавливаем группу пользователя как "admin"
        page.update()
        page.go('/admin')  # Переход на страницу админ-панели
    else:
        # Неверный пароль
        page.snack_bar = ft.SnackBar(ft.Text("Неверный пароль!", color=ft.colors.WHITE), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()
