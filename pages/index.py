import json
from flet import *

# Функция для загрузки конфигурации из config.json
def load_config():
    with open('./cwim-core-tgbt/config.json', 'r') as f:
        return json.load(f)

def tpl_index(page: Page):
    page.title = "Админ центр - Авторизация"

    # Инициализация состояния темы (из сессии)
    if page.session.get("theme_mode") is None:
        page.session.set("theme_mode", ThemeMode.LIGHT)  # По умолчанию светлая тема

    page.theme_mode = page.session.get("theme_mode")

    # Настройка центрального выравнивания содержимого страницы
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER

    # Загружаем пароль админа из конфигурации
    config = load_config()
    admin_password = config.get('admin_pass', '')

    # Поле для ввода пароля
    password_field = TextField(
        label="Введите пароль:",
        password=True,
        can_reveal_password=True,
        width=300,
        text_align=TextAlign.LEFT,
    )

    # Кнопка авторизации
    login_button = CupertinoFilledButton(
        "Войти",
        on_click=lambda e: authenticate(password_field.value, admin_password, page),
        width=200
    )

    # Переключатель темной/светлой темы
    theme_switch = Switch(
        thumb_icon=icons.SUNNY,
        value=page.theme_mode == ThemeMode.DARK,
        on_change=lambda e: toggle_theme(page, e.control.value) and [icons.SUNNY if theme == icons.MOOD else icons.SUNNY],
    )

    # AppBar с переключателем темы
    page.appbar = AppBar(
        title=Text("Админ центр"),
        center_title=True,
        bgcolor=colors.BLUE,
        actions=[
            theme_switch
        ]
    )

    # Добавляем элементы на страницу
    page.add(
        Column(
            [
                Text(
                    "Авторизация",
                    size=24,
                    weight=FontWeight.BOLD,
                    text_align=TextAlign.CENTER
                ),
                password_field,
                login_button,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )

    page.update()

def toggle_theme(page: Page, is_dark_mode: bool):
    """Переключает тему и сохраняет её в сессии."""
    theme = ThemeMode.DARK if is_dark_mode else ThemeMode.LIGHT
    page.session.set("theme_mode", theme)
    page.theme_mode = theme
    page.update()

def authenticate(input_password: str, admin_password: str, page: Page):
    """Проверяет введенный пароль и управляет сессией."""
    if input_password == admin_password:
        # Пароль верный, авторизуем пользователя
        page.snack_bar = SnackBar(Text("Авторизация успешна!"), bgcolor=colors.GREEN)
        page.snack_bar.open = True
        page.update()
        page.go('/admin')  # Переход на страницу админ-панели
    else:
        # Неверный пароль
        page.snack_bar = SnackBar(Text("Неверный пароль!", color=colors.WHITE), bgcolor=colors.RED)
        page.snack_bar.open = True
        page.update()

