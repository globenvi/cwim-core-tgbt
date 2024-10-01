from flet import *
from services.DatabaseService import JSONService
# Страница профиля
def tpl_profile(page: Page):
    user_group = page.session.get('user_group')  # Получаем группу пользователя

    # Если группа пользователя 'guest', отображаем сообщение
    if user_group == 'guest':
        return Column(
            controls=[
                Text("Вы должны войти, чтобы увидеть эту страницу.", size=20, color="red"),
                ElevatedButton("Войти", on_click=lambda e: page.go("/login"))
            ],
            alignment=MainAxisAlignment.CENTER,
            expand=True,
        )

    # Если пользователь не гость, получаем его данные
    db_service = JSONService()
    user_data = db_service.find_one('users', {'login': page.session.get('login')})  # Предполагаем, что логин пользователя хранится в сессии

    if user_data:
        profile_info = [
            Text(f"Логин: {user_data.get('login', 'Не указано')}", size=18),
            Text(f"Email: {user_data.get('email', 'Не указано')}", size=18),
            Text(f"Группа: {user_group}", size=18),
            # Добавьте другие данные по мере необходимости
        ]
    else:
        profile_info = [Text("Пользователь не найден.", size=20, color="red")]

    return Column(
        controls=[
            Text("Профиль пользователя", size=24, weight="bold"),
            Column(
                controls=profile_info,
                alignment=MainAxisAlignment.START
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        expand=True,
    )