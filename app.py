import os
import importlib
import json
from flet import Page, Text, Column
from colorama import Fore, Style, init

# Инициализация colorama
init(autoreset=True)

# Путь к папке шаблонов и другим файлам
TEMPLATES_DIR = "./cwim-core-tgbt/templates/Default"
ROUTES_FILE = "./cwim-core-tgbt/routes.json"
CONFIG_FILE = "./cwim-core-tgbt/config.json"
DATABASE_FILE = "./cwim-core-tgbt/datafiles/database.json"

# Переменная для хранения состояния отладки
DEBUG_MODE = False

def load_config():
    global DEBUG_MODE
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file {CONFIG_FILE} not found")
    with open(CONFIG_FILE, 'r') as config_file:
        config_data = json.load(config_file)
        DEBUG_MODE = config_data.get('core_settings', {}).get('debug_mode', False)
    print(f"{Fore.GREEN}Debug mode is {'enabled' if DEBUG_MODE else 'disabled'}{Style.RESET_ALL}")

def load_database():
    if not os.path.exists(DATABASE_FILE):
        raise FileNotFoundError(f"Database file {DATABASE_FILE} not found")
    with open(DATABASE_FILE, 'r') as db_file:
        return json.load(db_file)

def check_routes_file():
    if not os.path.exists(ROUTES_FILE):
        with open(ROUTES_FILE, "w") as f:
            json.dump({}, f)

def load_routes():
    check_routes_file()
    with open(ROUTES_FILE, "r") as f:
        return json.load(f)

def save_routes(routes):
    with open(ROUTES_FILE, "w") as f:
        json.dump(routes, f, indent=4)

def scan_templates():
    routes = load_routes()
    for file_name in os.listdir(TEMPLATES_DIR):
        if file_name.endswith(".py") and file_name != '__init__.py':
            module_name = file_name[:-3]
            route = f"/{module_name}"

            if route not in routes:
                routes[route] = {
                    "module": module_name,
                    "template": f"tpl_{module_name}",
                    "enabled": True,
                    "group_access": "all"
                }
                print(f"{Fore.GREEN}Маршрут {route} добавлен.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Маршрут {route} уже существует. Пропускаем.{Style.RESET_ALL}")

    save_routes(routes)

def check_access(route_info, user_group):
    required_groups = route_info.get('group_access', 'all').split(', ')
    if user_group == "admin":
        return True
    if 'all' not in required_groups and user_group not in required_groups:
        print(f"{Fore.RED}Доступ запрещен для группы: {user_group}. Требуется: {required_groups}{Style.RESET_ALL}")
        return False
    return True

def get_page(route, user_group="all"):
    routes = load_routes()
    print(f"{Fore.BLUE}Ищем маршрут для: {route}{Style.RESET_ALL}")

    if DEBUG_MODE:
        print(f"{Fore.BLUE}Существующие маршруты: {routes}{Style.RESET_ALL}")

    if route in routes:
        route_info = routes[route]
        if not route_info["enabled"]:
            print(f"{Fore.RED}Маршрут {route} отключен.{Style.RESET_ALL}")
            return None

        if not check_access(route_info, user_group):
            return None

        try:
            module = importlib.import_module(f"templates.Default.{route_info['module']}")
            template_func = getattr(module, route_info["template"])
            return template_func
        except Exception as e:
            print(f"{Fore.RED}Ошибка загрузки страницы {route}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Маршрут {route} не найден в routes.json.{Style.RESET_ALL}")
    return None

def router(page: Page):
    page.client_storage.clear()
    route = page.route or "/index"
    print(f"{Fore.BLUE}Текущий маршрут: {route}{Style.RESET_ALL}")

    user_group = page.session.get("user_group")  # По умолчанию группа "guest"
    print(f"{Fore.BLUE}Группа пользователя: {user_group}{Style.RESET_ALL}")

    page_template_func = get_page(route, user_group)

    # Очистка views и добавление новой страницы
    page.views.clear()
    if page_template_func:
        print(f"{Fore.GREEN}Отображаем страницу: {route}{Style.RESET_ALL}")
        page_view = page_template_func(page)  # Вызываем функцию, чтобы получить объект страницы
        page.views.append(page_view)  # Добавляем страницу в views
    else:
        print(f"{Fore.RED}Страница {route} не найдена или доступ запрещен.{Style.RESET_ALL}")
        page.views.append(Column([Text(f"Страница {route} не найдена или доступ запрещен.")]))

    page.update()  # Обновляем страницу для отображения изменений


def main(page: Page):
    load_config()  # Загружаем конфигурацию
    scan_templates()  # Сканируем шаблоны и обновляем маршруты

    if page.route == "/":
        page.route = "/index"

    page.on_route_change = lambda e: router(page)
    page.session.set("user_group", "guest")  # Устанавливаем группу пользователя

    router(page)

if __name__ == "__main__":
    import flet as ft
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
