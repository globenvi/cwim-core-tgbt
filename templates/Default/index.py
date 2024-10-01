from flet import *

def tpl_index(page):
    page.title = 'Главная страница'
    page.theme_mode = ThemeMode.SYSTEM
    # The value is automatically converted back to the original type
    login = page.client_storage.get("login")

    role = page.client_storage.get("role")

    print(f'Login: {login}\n, Role: {role}')
    # colors = ["red", "green", "blue"]
    page.add(
        Text('WELCOME TO HOME PAGE')
    )
