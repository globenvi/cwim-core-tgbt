import os
import importlib
import json
from flet import Page, Text, Column
from colorama import Fore, Style, init
import asyncio
import aiofiles  # Асинхронные операции с файлами

# Инициализация colorama
init(autoreset=True)

# Пути к файлам
TEMPLATES_DIR = "./web/templates/Default"
ROUTES_FILE = "./web/routes.json"
CONFIG_FILE = "./web/config.json"
DATABASE_FILE = "./web/datafiles/database.json"

# Переменная для хранения состояния отладки
DEBUG_MODE = False


# Загрузка конфигурации асинхронно
async def load_config():
    global DEBUG_MODE
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file {CONFIG_FILE} not found")
    async with aiofiles.open(CONFIG_FILE, 'r') as config_file:
        config_data = json.loads(await config_file.read())
        DEBUG_MODE = config_data.get('core_settings', {}).get('debug_mode', False)
    print(f"{Fore.GREEN}Debug mode is {'enabled' if DEBUG_MODE else 'disabled'}{Style.RESET_ALL}")


# Загрузка базы данных асинхронно
async def load_database():
    if not os.path.exists(DATABASE_FILE):
        raise FileNotFoundError(f"Database file {DATABASE_FILE} not found")
    async with aiofiles.open(DATABASE_FILE, 'r') as db_file:
        return json.loads(await db_file.read())


# Проверка наличия файла маршрутов
async def check_routes_file():
    if not os.path.exists(ROUTES_FILE):
        async with aiofiles.open(ROUTES_FILE, "w") as f:
            await f.write(json.dumps({}))


# Загрузка маршрутов
async def load_routes():
    await check_routes_file()
    async with aiofiles.open(ROUTES_FILE, "r") as f:
        return json.loads(await f.read())


# Сохранение маршрутов
async def save_routes(routes):
    async with aiofiles.open(ROUTES_FILE, "w") as f:
        await f.write(json.dumps(routes, indent=4))


# Сканирование шаблонов для добавления маршрутов
async def scan_templates():
    routes = await load_routes()
    for file_name in os.listdir(TEMPLATES_DIR):
        if file_name.endswith(".py") and file_name != '__init__.py':
            module_name = file_name[:-3]
            route = f"/{module_name}/"

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

    await save_routes(routes)


# Проверка доступа к маршруту
def check_access(route_info, user_group):
    required_groups = route_info.get('group_access', 'all').split(', ')
    if user_group == "admin":
        return True
    if 'all' not in required_groups and user_group not in required_groups:
        print(f"{Fore.RED}Доступ запрещен для группы: {user_group}. Требуется: {required_groups}{Style.RESET_ALL}")
        return False
    return True


# Получение страницы по маршруту
async def get_page(route, user_group="all"):
    routes = await load_routes()
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

            # Проверяем, является ли функция асинхронной
            if asyncio.iscoroutinefunction(template_func):
                return template_func
            else:
                print(f"{Fore.RED}Функция {route_info['template']} должна быть асинхронной.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка загрузки страницы {route}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Маршрут {route} не найден в routes.json.{Style.RESET_ALL}")
    return None


# Асинхронный роутер для обработки страниц
async def router(page: Page):
    # Извлекаем основной маршрут из page.route, игнорируя параметры
    base_route = page.route.split('?')[0]
    route = base_route or "/auth/"
    print(f"{Fore.BLUE}Текущий маршрут: {route}{Style.RESET_ALL}")

    user_group = page.session.get("user_group",)
    print(f"{Fore.BLUE}Группа пользователя: {user_group}{Style.RESET_ALL}")

    page_template_func = await get_page(route, user_group)

    # Очистка views и добавление новой страницы
    page.views.clear()
    if page_template_func:
        print(f"{Fore.GREEN}Отображаем страницу: {route}{Style.RESET_ALL}")

        # Если функция асинхронная, ждем ее результат
        page_view = await page_template_func(page)
        page.views.append(page_view)
    else:
        print(f"{Fore.RED}Страница {route} не найдена или доступ запрещен.{Style.RESET_ALL}")
        page.views.append(Column([Text(f"Страница {route} не найдена или доступ запрещен.")]))

    await page.update_async()


# Главная функция, которая запускает приложение
async def main(page: Page):
    await load_config()  # Загружаем конфигурацию
    await scan_templates()  # Сканируем шаблоны и обновляем маршруты

    # Устанавливаем начальную сессию, если она еще не определена
    if not page.session.get("user_group"):
        page.session.set("user_group", "guest")

    # Асинхронно обрабатываем изменения маршрутов
    page.on_route_change = lambda e: asyncio.create_task(router(page))

    # Первоначальный вызов роутера
    await router(page)


# Запуск приложения
if __name__ == "__main__":
    import flet as ft

    asyncio.run(ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=5000, assets_dir='assets'))
