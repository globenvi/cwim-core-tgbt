import json
from flet import *


# Функция для загрузки конфигурации из config.json
def load_config():
    with open('./config.json', 'r') as f:
        return json.load(f)


def tpl_login(page: Page):
    page.title = "Авторизация"
    page.vertical_alignment = MainAxisAlignment.CENTER

    # Загружаем пароль админа
    config = load_config()
    admin_password = config.get('admin_pass', '')

    # Поле для ввода пароля
    password_input = TextField(label="Пароль:", password=True, can_reveal_password=True, ref=TextField())

    # Индикатор загрузки
    progress_indicator = ProgressRing(visible=False)

    # Функция для обработки авторизации
    def login_action(e):
        progress_indicator.visible = True
        page.update()

        password = password_input.value
        if password == admin_password:
            print("Авторизация прошла успешно!")
            page.go('/admin')  # Переход на страницу админ-панели
        else:
            print("Неверный пароль!")
            page.add(Text("Неверный пароль, попробуйте еще раз.", color='red'))

        progress_indicator.visible = False
        page.update()

    # Кнопка для входа
    login_button = ElevatedButton("Войти", on_click=login_action)

    # Добавляем элементы на страницу
    page.add(
        Column([
            password_input,
            progress_indicator,
            login_button
        ], alignment="center")
    )
