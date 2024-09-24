import os
from flet import *


# Функция для получения списка модулей из папки
def get_modules():
    modules_dir = './modules_extra'
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)  # Создаем папку, если её нет
    return [f for f in os.listdir(modules_dir) if os.path.isfile(os.path.join(modules_dir, f))]


# Функция для отображения блока сессий
def session_block():
    # Здесь можно подключить реальные данные сессий
    sessions = [
        {"user": "user1", "status": "active", "time": "12:30"},
        {"user": "user2", "status": "inactive", "time": "10:00"},
    ]
    return Column([
        Text(f"Пользователь: {session['user']} | Статус: {session['status']} | Время: {session['time']}")
        for session in sessions
    ], spacing=10)


# Функция для отображения блока модулей с возможностью включения/выключения
def modules_block():
    modules = get_modules()

    def toggle_module(e, module_name):
        # Логика для включения/выключения модуля
        # Здесь можно управлять модулями, изменяя их статус (включен/выключен)
        print(f"Модуль {module_name} переключен")

    return Column([
        Row([
            Text(module, expand=1),
            Switch(label="Включить", on_change=lambda e, module_name=module: toggle_module(e, module_name))
        ], alignment=MainAxisAlignment.SPACE_BETWEEN)
        for module in modules
    ], spacing=10)


# Функция для админ-панели с блоками и пагинацией
def tpl_admin(page: Page):
    page.title = "Админ центр"
    page.theme_mode = ThemeMode.SYSTEM

    # Создаем пагинацию для переключения между блоками
    blocks = {
        "Сессии": session_block(),
        "Модули": modules_block()
    }

    def change_page(e):
        page.controls.clear()
        page.controls.append(create_page_content(e.control.value))
        page.update()

    # Переключатель страниц (блоков)
    page_selector = Dropdown(
        options=[dropdown.Option("Сессии"), dropdown.Option("Модули")],
        on_change=change_page,
        width=150,
    )

    # Функция для создания контента страницы
    def create_page_content(selected_page):
        if selected_page == "Сессии":
            return Column([
                Text("Активные сессии", size=20, weight=FontWeight.BOLD),
                session_block(),
            ], alignment=MainAxisAlignment.CENTER)
        elif selected_page == "Модули":
            return Column([
                Text("Управление модулями", size=20, weight=FontWeight.BOLD),
                modules_block(),
            ], alignment=MainAxisAlignment.CENTER)

    # Установка стартовой страницы
    page.add(
        Column(
            [
                page_selector,
                create_page_content("Сессии"),  # Начальная страница "Сессии"
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    page.update()