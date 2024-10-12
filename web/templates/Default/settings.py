from anyio.abc import value
from flet import *

from web.templates.Default.auth import db_service


def tpl_settings(page: Page):
    # Настройка страницы
    page.title = "Настройки"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Заголовок страницы
    header = Text("Настройки", size=20, text_align="left")

    user_settings = db_service.find_one('user_settings', {'tgid': int(page.session.get('tgid'))})

    if user_settings.get('theme_dark_mode'):
        page.theme_mode = ThemeMode.DARK
    else:
        page.theme_mode = ThemeMode.LIGHT

    # Переключатели настроек
    dark_mode_switch = Switch(label="Темный режим", value=False,
                              on_change=lambda e: toggle_dark_mode())
    notifications_switch = Switch(label="Уведомления", value=True,
                                  on_change=lambda e: toggle_notifications())

    if not db_service.find_one('user_settings', {'tgid': int(page.session.get('tgid'))}):
        db_service.create('user_settings',
                          {'tgid': page.session.get('tgid'), 'theme_dark_mode': True, 'notifications': True})
    else:

        # Переключатели настроек
        dark_mode_switch = CupertinoSwitch(label="Темный режим", value= user_settings.get('theme_dark_mode'), on_change=lambda e: toggle_dark_mode(), active_color=colors.GREEN)
        notifications_switch = CupertinoSwitch(label="Уведомления", value= user_settings.get('notifications'), on_change=lambda e: toggle_notifications(), active_color=colors.GREEN)


    # Кнопка сохранения
    save_button = CupertinoFilledButton(text="Сохранить", icon=icons.SAVE, on_click=lambda e: save_settings())
    auto_update_download_app_switch = CupertinoSwitch(label='Автозагрузка обновлений WEB-UI', value=user_settings.get('web_core_updates_download_auto'),
                                             active_color=colors.GREEN,
                                             visible=True if page.session.get('user_group') == 'admin' else False)
    auto_update_install_app_switch = CupertinoSwitch(label='Автоустановка обновлений WEB-UI', value=user_settings.get('web_core_updates_install_auto'),
                                            active_color=colors.GREEN,
                                            visible=True if page.session.get('user_group') == 'admin' else False)

    app_version = Text(value="1.016")

    # Обработчик переключения темного режима
    def toggle_dark_mode():
        page.theme_mode = ThemeMode.DARK if dark_mode_switch.value else ThemeMode.LIGHT
        page.update()

    # Обработчик переключения уведомлений
    def toggle_notifications():
        print(f"Уведомления {'включены' if notifications_switch.value else 'выключены'}")

    # Обработчик сохранения настроек
    def save_settings():
        db_service.update('user_settings', user_settings.get('id'), {
            'theme_dark_mode': dark_mode_switch.value,
            'notifications' : notifications_switch.value,
            'web_core_updates_download_auto': auto_update_download_app_switch.value,
            'web_core_updates_install_auto': auto_update_install_app_switch.value
        })
        page.snack_bar = SnackBar(content=Text("Настройки успешно сохранены"), open=True)
        page.update()

    # Определение формы настроек
    settings_column = Column(
        controls=[
            header,
            dark_mode_switch,
            notifications_switch,
            auto_update_download_app_switch,
            auto_update_install_app_switch,
            save_button,
            Divider(),
            app_version
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=10,
    )

    app_info_column = Column(
        [
            app_version
        ],
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Купертино-бар внизу
    cupertino_bar = Row(
        controls=[

            IconButton(icon=icons.SETTINGS, tooltip="Настройки", on_click=lambda e: page.go('/settings/'), bgcolor=colors.PRIMARY, icon_color=colors.ON_PRIMARY),
            IconButton(icon=icons.MESSENGER, tooltip="Чат", on_click=lambda e: page.go('/chat/')),
            IconButton(icon=icons.PERSON_4, tooltip="Профиль", on_click=lambda e: page.go('/profile/')),
            IconButton(icon=icons.BROWSER_UPDATED, tooltip="Мои сервера", visible=True, on_click=lambda e: page.go('/servers/')),
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
                    spacing=25,
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