import os
import geoip2.database
from flet import *

# Фиктивные данные о сессиях для примера
sessions_data = [
    {"user": "user1", "ip": "192.0.2.1", "os": "Windows 10", "status": "active"},
]

# Функция для получения местоположения по IP
def get_ip_location(ip):
    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')  # Путь к вашей базе данных GeoLite2
        response = reader.city(ip)
        return f"{response.city.name}, {response.country.name}"
    except Exception as e:
        print(f"Ошибка при получении местоположения: {e}")
        return "Неизвестно"

# Функция для бана/разбана пользователей
def toggle_ban(user):
    for session in sessions_data:
        if session['user'] == user:
            session['status'] = "banned" if session['status'] == "active" else "active"
            return session['status']
    return None

# Функция для отображения блока с активными сессиями
def session_block():
    rows = []
    for session in sessions_data:
        location = get_ip_location(session['ip'])
        ban_button = ElevatedButton(
            "Забанить" if session['status'] == "active" else "Разбанить",
            on_click=lambda e, user=session['user']: update_session_status(user),
            bgcolor=colors.RED if session['status'] == "active" else colors.GREEN
        )
        rows.append(
            Row([
                Text(f"Пользователь: {session['user']} | IP: {session['ip']} | ОС: {session['os']} | Локация: {location} | Статус: {session['status']}"),
                ban_button
            ], alignment=MainAxisAlignment.SPACE_BETWEEN)
        )

    return Column(rows, spacing=10)

# Функция для обновления статуса сессии
def update_session_status(user):
    new_status = toggle_ban(user)
    print(f"Статус пользователя {user} изменен на: {new_status}")

# Функция для отображения блока управления модулями
def modules_block():
    modules = get_modules()

    def toggle_module(e, module_name):
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

    page.add(
        Column(
            [
                Text("Админ Панель", size=20, weight=FontWeight.BOLD),
                session_block(),
                modules_block(),
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

    page.update()

# Запуск приложения
def main(page: Page):
    tpl_admin(page)

app(target=main)
