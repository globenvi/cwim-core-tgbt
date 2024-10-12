from flet import *

from web.templates.Default.auth import db_service


def tpl_profile(page: Page):
    # Настройка страницы
    page.title = "Профиль"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Заголовок страницы
    header = Text("Профиль", size=20, text_align="left")

    user_settings = db_service.find_one('user_settings', {'tgid': int(page.session.get('tgid'))})

    if user_settings.get('theme_dark_mode'):
        page.theme_mode = ThemeMode.DARK
    else:
        page.theme_mode = ThemeMode.LIGHT


    # Кнопка сохранения
    save_button = CupertinoFilledButton(text="Сохранить", icon=icons.SAVE, on_click=lambda e: save_settings())

    user_id = Text(value=f"ID: {page.session.get('id')}")
    telegramID = Text(value=f"Telegram ID: {page.session.get('tgid')}")
    username = Text(value=f"Username: {page.session.get('uname')}")
    fist_name = Text(value=f"Имя: {page.session.get('fname')}")
    lastname = Text(value=f"Фамилия: {page.session.get('lname')}")
    user_group = Text(value=f"Группа пользователя: {page.session.get('user_group')}")



    # Обработчик сохранения настроек
    def save_settings():
        page.snack_bar = SnackBar(content=Text("Настройки успешно сохранены"), open=True)
        page.update()

    # Определение формы настроек
    settings_column = Column(
        controls=[
            header,
            user_id,
            telegramID,
            username,
            fist_name,
            lastname,
            user_group,
            save_button

        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.START,
        spacing=20,
    )

    # Купертино-бар внизу
    cupertino_bar = Row(
        controls=[
            IconButton(icon=icons.SETTINGS, tooltip="Настройки", on_click=lambda e: page.go('/settings/')),
            IconButton(icon=icons.MESSENGER, tooltip="Чат", on_click=lambda e: page.go('/chat/')),
            IconButton(icon=icons.PERSON_4, tooltip="Профиль", on_click=lambda e: page.go('/profile/'), bgcolor=colors.PRIMARY, icon_color=colors.ON_PRIMARY),
            IconButton(icon=icons.BROWSER_UPDATED, tooltip="Мои сервера",
                       visible=True,
                       on_click=lambda e: page.go('/servers/')),
        ],
        alignment=MainAxisAlignment.CENTER,
        spacing=10,
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
                    spacing=15,
                )
            ),
            Container(
                height=60,
                padding=10,
                border_radius=10,
                bgcolor=colors.ON_SECONDARY,
                alignment=alignment.bottom_center,
                content=cupertino_bar
            )
        ],
        expand=True  # Позволяем контейнеру занимать всю доступную высоту
    )