import os
import json
from http.cookies import SimpleCookie
from flet import Page, Column, Text, TextField, ElevatedButton, get_app, Router
import importlib
import asyncio

# Загрузка маршрутов из routes.json
def load_routes():
    with open('routes.json', 'r') as f:
        return json.load(f)

# Проверка доступа к странице
def check_access(route_info, user_group):
    return route_info['group_access'] == 'all' or route_info['group_access'] == user_group

# Установка cookie для сессии
def set_session_cookie(page, session_id, user_group):
    cookie = SimpleCookie()
    cookie['session_id'] = session_id
    cookie['user_group'] = user_group
    cookie['session_id']['path'] = '/'
    cookie['user_group']['path'] = '/'
    page.response_headers['Set-Cookie'] = cookie.output(header='', sep='').strip()

# Получение user_group из cookie
def get_user_group_from_cookie(page):
    user_group = "guest"  # Значение по умолчанию
    if 'HTTP_COOKIE' in page.request_headers:
        cookie_string = page.request_headers['HTTP_COOKIE']
        cookie = SimpleCookie(cookie_string)
        if 'user_group' in cookie:
            user_group = cookie['user_group'].value
    return user_group

# Инициализация маршрутов и загрузка модулей
def init_routes(page):
    routes = load_routes()
    for route, info in routes.items():
        if info['enabled']:
            module = importlib.import_module(f"pages.{info['module']}")
            page.router.add_route(route, lambda p, m=module, t=info['template']: getattr(m, t)(p))

# Главная функция приложения
async def main(page: Page):
    # Инициализация маршрутов
    init_routes(page)

    # Получаем user_group из cookie
    user_group = get_user_group_from_cookie(page)

    # Устанавливаем маршрут по умолчанию
    if not check_access(load_routes()['/index'], user_group):
        await page.goto('/login')  # Перенаправляем на страницу входа
    else:
        await page.goto('/index')

# Запуск приложения
def run_app():
    app = get_app()
    app.start(main)

if __name__ == "__main__":
    run_app()
