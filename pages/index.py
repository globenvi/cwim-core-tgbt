import json
from flet import *


# Функция для загрузки конфигурации из config.json
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def tpl_index(page: Page):
    page.title = "Авторизация"
    page.theme_mode = ThemeMode.SYSTEM

    # Загружаем пароль админа
    config = load_config()
    admin_password = config.get('admin_pass', '')

    # Поле для ввода пароля
    password_field = TextField(label="Пароль:", password=True, can_reveal_password=True)
    login_button = ElevatedButton("Войти", on_click=lambda e: authenticate(password_field.value, admin_password, page))

    # Добавляем элементы на страницу
    page.add(password_field, login_button)


def authenticate(input_password: str, admin_password: str, page: Page):
    """Проверяет введенный пароль и управляет сессией."""
    if input_password == admin_password:
        # Пароль верный, авторизуем пользователя
        print("Авторизация прошла успешно!")
        page.go('/admin')  # Переход на страницу админ-панели
    else:
        # Неверный пароль
        print("Неверный пароль!")
        page.add(Text("Неверный пароль, попробуйте еще раз.", color='red'))
        page.update()
