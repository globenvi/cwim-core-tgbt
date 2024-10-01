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
DATABASE_FILE = "./datafiles/database.json"

# Переменная для хранения состояния отладки
DEBUG_MODE = False

def load_config():
    global DEBUG_MODE
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file {CONFIG_FILE} not found")

    with open(CONFIG_FILE, 'r') as config_file:
        config_data = json.load(config_file)

    # Проверяем режим отладки
    DEBUG_MODE = config_data.get('core_settings', {}).get('debug_mode', False)
    print(f"{Fore.GREEN}Debug mode is {'enabled' if DEBUG_MODE else 'disabled'}{Style.RESET_ALL}")

def load_database():
    if not os.path.exists(DATABASE_FILE):
        raise FileNotFoundError(f"Database file {DATABASE_FILE} not found")

    with open(DATABASE_FILE, 'r') as db_file:
        return json.load(db_file)

# Загрузка базы данных
database = load_database()

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
def scan_templates():
    routes = load_routes()
    for file_name in os.listdir(TEMPLATES_DIR):
        if file_name.endswith(".py"):
            module_name = file_name[:-3]
            route = f"/{module_name}"

            # Проверяем, существует ли маршрут уже в routes.json
            if route in routes:
                print(f"{Fore.YELLOW}Маршрут {route} уже существует. Пропускаем.{Style.RESET_ALL}")
            else:
                routes[route] = {
                    "module": module_name,
                    "template": f"tpl_{module_name}",
                    "enabled": True,
                    "group_access": "all"  # Можно указать группы для каждой страницы
                }
                print(f"{Fore.GREEN}Маршрут {route} добавлен.{Style.RESET_ALL}")

    save_routes(routes)

# Проверка доступа к странице
def check_access(route_info, user_group):
    required_groups = [grp.strip() for grp in route_info.get('group_access', 'all').split(",")]
    user_permissions = []

    # Проверяем, находится ли user_group в базе данных
    # Предполагается, что 'users_groups' является списком с одним элементом, содержащим группы
    users_groups = database.get("users_groups", [])
    if users_groups:
        users_groups_dict = users_groups[0]  # Извлекаем первый элемент списка
        group_info = users_groups_dict.get(user_group, [])
        if group_info:
            user_permissions = group_info[0].get('permissions', [])

    # Если у пользователя есть права на все страницы
    if 'all' in user_permissions:
        print(f"{Fore.GREEN}Доступ разрешен для {user_group} (все разрешения){Style.RESET_ALL}")
        return True

    # Проверяем, имеет ли пользователь доступ к странице на основе групп
    if 'all' in required_groups or user_group in required_groups:
        print(f"{Fore.GREEN}Доступ разрешен для {user_group}{Style.RESET_ALL}")
        return True

    print(f"{Fore.RED}Доступ запрещен для группы {user_group}. Требуются группы: {required_groups}{Style.RESET_ALL}")
    return False

# Получение страницы по маршруту
def get_page(route, user_group="guest"):
    routes = load_routes()
    print(f"{Fore.BLUE}Ищем маршрут для: {route}{Style.RESET_ALL}")

    # Отладка: Выводим все маршруты для проверки
    if DEBUG_MODE:
        print(f"{Fore.BLUE}Существующие маршруты: {routes}{Style.RESET_ALL}")

    if route in routes:
        route_info = routes[route]
        print(f"{Fore.GREEN}Маршрут найден: {route}, модуль: {route_info['module']}, шаблон: {route_info['template']}{Style.RESET_ALL}")

        if not route_info["enabled"]:
            print(f"{Fore.RED}Маршрут {route} отключен.{Style.RESET_ALL}")
            return None

        # Проверяем доступ к странице
        if not check_access(route_info, user_group):
            return None

        try:
            # Импортируем модуль страницы из шаблонов
            module = importlib.import_module(f"cwim_core_tgbt.templates.Default.{route_info['module']}")
            template_func = getattr(module, route_info["template"])
            return template_func
        except Exception as e:
            print(f"{Fore.RED}Ошибка загрузки страницы {route}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Маршрут {route} не найден в routes.json.{Style.RESET_ALL}")
    return None

# Функция роутинга
def router(page: Page):
    # Получаем маршрут из запроса, по умолчанию перенаправляем на "/index"
    route = page.route or "/index"
    print(f"{Fore.BLUE}Текущий маршрут: {route}{Style.RESET_ALL}")

    # Получаем группу пользователя (по умолчанию "guest")
    user_group = page.session.get("user_group") or "guest"  # Исправлено: убран второй аргумент
    print(f"{Fore.BLUE}Группа пользователя: {user_group}{Style.RESET_ALL}")

    # Получаем шаблон страницы по маршруту
    page_template = get_page(route, user_group)

    if page_template:
        print(f"{Fore.GREEN}Отображаем страницу: {route}{Style.RESET_ALL}")
        page.controls.clear()
        page_template(page)  # Отрисовка страницы
    else:
        print(f"{Fore.RED}Страница {route} не найдена или доступ запрещен.{Style.RESET_ALL}")
        page.controls.clear()
        page.controls.append(Column([Text(f"Страница {route} не найдена или доступ запрещен.")]))
        page.update()

# Пример инициализации приложения Flet
def main(page: Page):
    try:
        load_config()  # Загружаем конфигурацию
    except Exception as e:
        print(f"{Fore.RED}Ошибка загрузки конфигурации: {e}{Style.RESET_ALL}")
        page.controls.append(Column([Text("Ошибка загрузки конфигурации.")]))
        page.update()
        return

    try:
        scan_templates()  # Сканируем шаблоны и обновляем маршруты
    except Exception as e:
        print(f"{Fore.RED}Ошибка сканирования шаблонов: {e}{Style.RESET_ALL}")
        page.controls.append(Column([Text("Ошибка сканирования шаблонов.")]))
        page.update()
        return

    # Устанавливаем начальный маршрут, если он не задан
    if page.route == "/":
        page.route = "/index"

    # Обработчик события изменения маршрута
    async def on_route_change(e):
        router(page)

    # Слушаем изменения маршрута
    page.on_route_change = on_route_change

    # Устанавливаем группу пользователя в сессии (можно настраивать через авторизацию)
    page.session.set("user_group", "guest")  # Группу можно изменить на "admin" или другую

    # Запуск роутера
    router(page)

# Запуск Flet
if __name__ == "__main__":
    import flet as ft
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=57060)
