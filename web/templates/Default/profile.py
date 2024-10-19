import asyncio
from urllib.parse import urlparse, parse_qs
from flet import *
from watchfiles import awatch

from services.DatabaseService import JSONService
from core.controllers.UserController import User

db_service = JSONService()

def extract_query_params(page: Page):
    # Извлечение URL из page.route
    url = page.route
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
    return query_params

async def tpl_profile(page: Page):
    # Настройка страницы
    page.title = "Настройки"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    tgid = extract_query_params(page).get('tgid')

    user_instance = User(tgid=int(tgid))
    user_data = await user_instance.read_user()
    user_settings = await user_instance.read_user_settings()

    # Определяем URL аватара
    avatar_url = user_data.get('avatar_url')  # Предположим, что 'avatar_url' возвращается из read_user

    if user_settings.get('dark_mode'):
        page.theme_mode = ThemeMode.DARK
    else:
        page.theme_mode = ThemeMode.LIGHT

    async def save_user_data(e):
        updated_user_data = {
            "first_name": user_settings_change_first_name_input.value,
            "last_name": user_settings_change_last_name_input.value
        }
        updated_user_settings = {
            "dark_mode": user_settings_theme_switcher.value,
            "notifications": user_settings_notification_switcher.value,
            "show_uid": user_settings_show_uid_switcher.value,
        }
        await user_instance.update_user(updated_user_data)
        await user_instance.update_user_settings(updated_user_settings)
        page.snack_bar = SnackBar(content=Text("Настройки успешно сохранены"), open=True, bgcolor=colors.GREEN)
        page.update()

    async def change_theme_mode(e):
        if user_settings_theme_switcher.value:
            user_settings_theme_switcher.thumb_icon = icons.SHIELD_MOON
            page.theme_mode = ThemeMode.DARK
        else:
            user_settings_theme_switcher.thumb_icon = icons.SUNNY_SNOWING
            page.theme_mode = ThemeMode.LIGHT
        page.update()  # Обновление страницы для применения темы

    user_settings_theme_switcher = Switch(
        label='Dark Mode',
        active_color=colors.GREEN,
        value=user_settings.get('dark_mode'),
        on_change=lambda e: asyncio.run(change_theme_mode(e)),
        thumb_icon=icons.SUNNY
    )
    user_settings_notification_switcher = Switch(label='Уведомления', active_color=colors.GREEN, value=user_settings.get('notifications'))
    user_settings_show_uid_switcher = Switch(label='Показывать ID в настройках', active_color=colors.GREEN, value=user_settings.get('show_uid'))

    user_settings_save_button = CupertinoFilledButton(text="Сохранить", icon=icons.SAVE, on_click=lambda e: asyncio.run(save_user_data(e)))

    user_settings_change_first_name_input = TextField(label="Имя", expand_loose=True, visible=True, value=user_data.get('first_name'))
    user_settings_change_last_name_input = TextField(label="Фамилия", expand_loose=True, visible=True, value=user_data.get('last_name'))
    user_settings_group_text_output = TextField(f'Группа: {user_data.get("user_group")}', disabled=True)  # Исправлено

    # Определяем инициалы, если аватара нет
    if avatar_url:
        avatar_image = Image(src=avatar_url, width=100, height=100)  # Настройте размер по вашему усмотрению
    else:
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        initials = f"{first_name[0].upper()}.{last_name[0].upper()}" if first_name and last_name else "??"
        avatar_image = Text(initials, size=40, weight='bold')  # Можно настроить размер и стиль текста

        def pick_files_result(e: FilePickerResultEvent):
            selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            selected_files.update()

        pick_files_dialog = FilePicker(on_result=pick_files_result)
        selected_files = Text()

        page.overlay.append(pick_files_dialog)

    settings_column = Column(
        [
            Text('Настройки', size=20, weight='20'),
            Column(
                [
                    avatar_image,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=10
            ),
            user_settings_change_first_name_input,
            user_settings_change_last_name_input,
            user_settings_group_text_output,
            Divider(),
            user_settings_theme_switcher,
            user_settings_notification_switcher,
            user_settings_show_uid_switcher,
            user_settings_save_button
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=10
    )

    # Основной контейнер с прокруткой и фиксированной нижней панелью
    return Column(
        controls=[
            Container(
                expand=True,
                content=Column(
                    scroll=ScrollMode.AUTO,
                    controls=[
                        Container(
                            bgcolor=colors.ON_SECONDARY,
                            padding=20,
                            margin=10,
                            border_radius=10,
                            content=settings_column,
                            alignment=alignment.center
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=25,
                )
            ),
        ],
        expand=True  # Позволяем контейнеру занимать всю доступную высоту
    )
