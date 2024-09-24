import os
import importlib
import json
from flet import Page, Text, Column, TextField, ElevatedButton

# Путь к папке со страницами
PAGES_DIR = "./cwim-core-tgbt/pages"

# Путь к файлу с роутами
ROUTES_FILE = "./cwim-core-tgbt/routes.json"

# Проверка наличия файла и его создание, если не существует
def check_routes_file():
    if not os.path.exists(ROUTES_FILE):
        with open(ROUTES_FILE, "w") as f:
            json.dump({}, f)

# Чтение существующих роутов из файла
def load_routes():
    check_routes_file()
    with open(ROUTES_FILE, "r") as f:
        return json.load(f)

# Сохранение роутов в файл
def save_routes(routes):
    with open(ROUTES_FILE, "w") as f:
        json.dump(routes, f, indent=4)

# Сканирование папки на наличие страниц
def scan_pages():
    routes = load_routes()
    for file_name in os.listdir(PAGES_DIR):
        if file_name.endswith(".py"):
            module_name = file_name[:-3]
            try:
                module = importlib.import_module(f"pages.{module_name}")
                for attr in dir(module):
                    if attr.startswith("tpl_"):
                        route = f"/{module_name}"
                        routes[route] = {
                            "module": module_name,
                            "template": attr,
                            "enabled": True,
                            "group_access": "all"
                        }
                        print(f"Маршрут {route} добавлен.")
            except Exception as e:
                print(f"Ошибка импорта {module_name}: {e}")
    save_routes(routes)

# Получение страницы по маршруту
def get_page(route, user_group="all"):
    routes = load_routes()
    if route in routes:
        route_info = routes[route]
        if not route_info["enabled"]:
            return None  # Страница отключена
        if route_info["group_access"] != "all" and route_info["group_access"] != user_group:
            return None  # Доступ запрещен
        try:
            module = importlib.import_module(f"pages.{route_info['module']}")
            template_func = getattr(module, route_info["template"])
            return template_func
        except Exception as e:
            print(f"Ошибка загрузки страницы {route}: {e}")
    return None

# Функция для проверки авторизации пользователя
def is_authorized(page):
    return page.session.get('user_id') is not None

# Функция для установки куки после авторизации
def set_auth_cookie(page, user_id):
    page.session['user_id'] = user_id
    page.session['user_group'] = 'admin'  # Здесь вы можете задать группу пользователя

# Функция для проверки доступа к маршруту
def check_access(route_info, user_group):
    return route_info['group_access'] == 'all' or route_info['group_access'] == user_group

# Обновленная функция роутинга
def router(page: Page):
    route = page.route or "/index"
    user_group = page.session.get("user_group") or "all"

    if not is_authorized(page) and route != '/login':
        page.go('/login')  # Перенаправляем на страницу логина
        return

    page_template = get_page(route, user_group)

    if page_template:
        if not check_access(page_template, user_group):
            page.controls.clear()
            page.controls.append(Column([Text("Доступ запрещен.")]))
            page.update()
            return

        page.controls.clear()
        page_template(page)
    else:
        page.controls.clear()
        page.controls.append(Column([Text(f"Страница {route} не найдена.")]))
        page.update()

# Пример функции авторизации
def authenticate(input_password: str, page: Page):
    # Замените 'your_admin_password' на свой пароль
    if input_password == 'your_admin_password':
        set_auth_cookie(page, 'user_id_123')  # Установите уникальный идентификатор пользователя
        page.go('/admin')  # Перейти на страницу админ-панели
    else:
        print("Неверный пароль!")

# Шаблон страницы логина
def tpl_login(page: Page):
    password_input = TextField(label="Пароль", password=True)  # Создаем поле для пароля

    def login_action(e):
        password = password_input.value
        authenticate(password, page)

    # Добавляем элементы управления на страницу
    page.controls.append(Column([
        Text("Логин"),
        password_input,
        ElevatedButton("Войти", on_click=login_action)
    ]))
    page.update()

# Пример инициализации приложения Flet
def main(page: Page):
    scan_pages()

    if page.route == "/":
        page.route = "/index"

    page.on_route_change = lambda e: router(page)

    # Запуск роутера
    router(page)

# Запуск Flet
if __name__ == "__main__":
    import flet as ft
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
