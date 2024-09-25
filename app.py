import os
import importlib
import json
from flet import Page, Text, Column

# Путь к папке со страницами
PAGES_DIR = "./cwim-core-tgbt/pages"

# Путь к файлу с роутами
ROUTES_FILE = "./cwim-core-tgbt/routes.json"

# Путь к файлу конфигурации
CONFIG_FILE = "./cwim-core-tgbt/config.json"


# Загрузка конфигурации
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


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

                        # Проверяем, существует ли маршрут уже в routes.json
                        if route in routes:
                            print(f"Маршрут {route} уже существует. Пропускаем создание новой записи.")
                        else:
                            routes[route] = {
                                "module": module_name,
                                "template": attr,
                                "enabled": True,
                                "group_access": "all"  # Можно указать группы для каждой страницы
                            }
                            print(f"Маршрут {route} добавлен с доступом для всех групп.")
            except Exception as e:
                print(f"Ошибка импорта {module_name}: {e}")
    save_routes(routes)


# Динамический импорт шаблона
def dynamic_import_template(template_path):
    """Динамически загружает шаблон по указанному пути."""
    try:
        module = importlib.import_module(template_path.replace("/", "."))
        return module
    except ModuleNotFoundError:
        print(f"Шаблон {template_path} не найден.")
        return None


# Получение страницы по маршруту
def get_page(route, user_group="all"):
    routes = load_routes()
    print(f"Ищем маршрут для: {route}")

    # Отладка: Выводим все маршруты для проверки
    print("Существующие маршруты:", routes)

    if route in routes:
        route_info = routes[route]
        print(f"Маршрут найден: {route}, модуль: {route_info['module']}, шаблон: {route_info['template']}")

        if not route_info["enabled"]:
            print(f"Маршрут {route} отключен.")
            return None  # Страница отключена

        # Проверяем доступ к странице по группе пользователя
        if route_info["group_access"] != "all" and route_info["group_access"] != user_group:
            print(f"Доступ запрещен для группы: {user_group}")
            return None

        # Динамически загружаем шаблон
        config = load_config()
        template_path = f"templates.{config['core_settings']['default_template']}.{route_info['template']}"
        module = dynamic_import_template(template_path)

        if module is not None:
            template_func = getattr(module, 'tpl_' + route_info['module'], None)
            if template_func:
                return template_func
            else:
                print(f"Функция для шаблона {template_path} не найдена.")
    else:
        print(f"Маршрут {route} не найден в routes.json.")
    return None


# Функция роутинга
def router(page: Page):
    # Получаем маршрут из запроса, по умолчанию перенаправляем на "/index"
    route = page.route or "/index"
    print(f"Текущий маршрут: {route}")

    # Получаем группу пользователя (по умолчанию "all")
    user_group = page.session.get("user_group") or "all"  # Исправлено: убран третий аргумент
    print(f"Группа пользователя: {user_group}")

    # Получаем шаблон страницы по маршруту
    page_template = get_page(route, user_group)

    if page_template:
        print(f"Отображаем страницу: {route}")
        page.controls.clear()
        page_template(page)
    else:
        print(f"Страница {route} не найдена или доступ запрещен.")
        page.controls.clear()
        page.controls.append(Column([Text(f"Страница {route} не найдена или доступ запрещен.")]))
        page.update()


# Пример инициализации приложения Flet
def main(page: Page):
    # Сканируем страницы при старте приложения
    scan_pages()

    # Устанавливаем начальный маршрут, если он не задан
    if page.route == "/":
        page.route = "/index"
        page.go('/index')

    # Обработчик события перехода по маршруту
    def on_route_change(e):
        router(page)

    # Слушаем изменения маршрута
    page.on_route_change = on_route_change

    # Устанавливаем группу пользователя в сессии (можно настраивать через авторизацию)
    page.session.set("user_group", "all")  # Группу можно изменить на "admin" или другую

    # Запуск роутера
    router(page)


# Запуск Flet
if __name__ == "__main__":
    import flet as ft

    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
