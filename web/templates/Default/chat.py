from flet import *

from core.handlers.users_commands import db_service


def tpl_chat(page: Page):
    # Настройка страницы
    page.title = "Чат"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Получаем информацию о пользователе
    user = db_service.find_one('users', {'tgid': int(page.session.get('tgid'))})
    user_name = user.get('username', 'User')
    user_avatar = user.get('avatar_url', None)  # Ссылка на аватар пользователя, если есть

    # Функция для получения инициалов пользователя
    def get_initials(name):
        name_parts = name.split()
        if len(name_parts) > 1:
            return name_parts[0][0] + name_parts[1][0]
        return name_parts[0][0]

    # Список сообщений чата
    messages_column = Column(scroll=ScrollMode.AUTO, expand=True)

    # Поле для ввода текста сообщения
    message_input = TextField(
        hint_text="Введите сообщение...",
        expand=True,
        autofocus=True
    )

    # Функция для отправки сообщения
    def send_message(_e=None):
        message = message_input.value.strip()
        if message:
            # Отправляем сообщение с информацией о пользователе
            page.pubsub.send_all({'message': message, 'user': user_name, 'avatar': user_avatar})
            message_input.value = ""
            page.update()

    # Функция для обновления чата при получении нового сообщения
    def on_message_received(data):
        avatar_url = data.get('avatar')
        avatar = None

        # Если есть аватар, то выводим изображение, иначе инициалы
        if avatar_url:
            avatar = CircleAvatar(foreground_image_url=avatar_url)
        else:
            initials = get_initials(data['user'])
            avatar = CircleAvatar(content=Text(initials), bgcolor=colors.BLUE)

        # Оформление сообщения в виде "блока"
        message_bubble = Container(
            content=Text(f"{data['message']}"),  # Убрали wrap
            padding=10,
            border_radius=12,
            width=280,  # Ограничиваем максимальную ширину сообщения
            bgcolor=colors.ON_SECONDARY,
            margin=margin.only(left=5),
        )

        # Создание контейнера для сообщения с аватаром
        new_message = Container(
            content=Row(
                controls=[
                    avatar,  # Аватар или инициалы
                    message_bubble  # Сообщение в виде блока
                ],
                alignment=MainAxisAlignment.START,
                vertical_alignment=CrossAxisAlignment.CENTER
            ),
            margin=margin.only(bottom=10),
            padding=padding.only(left=10, right=10),
        )
        messages_column.controls.append(new_message)
        page.update()

    # Подключаем обработчик для pubsub
    page.pubsub.subscribe(on_message_received)

    # Кнопка для отправки сообщения
    send_button = IconButton(
        icon=icons.SEND,
        on_click=send_message,

    )

    # Обработка отправки при нажатии Enter
    message_input.on_submit = send_message

    # Верхняя часть страницы с заголовком
    top_container = Container(
        content=Column(
            controls=[
                Text("Чат сообщества", size=20),
                Divider()
            ],
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

    # Нижняя часть страницы с полем ввода и кнопкой отправки
    bottom_container = Container(
        content=Row(
            controls=[
                message_input,
                send_button
            ],
            alignment=MainAxisAlignment.CENTER,
            expand=True
        ),
        alignment=alignment.bottom_center,
        padding=10,
        bgcolor=colors.BACKGROUND  # Фиксируем нижнюю часть контейнера
    )

    # Основной макет страницы
    return Column(
        controls=[
            top_container,
            Container(
                content=messages_column,
                expand=True
            ),
            Container(
                alignment=alignment.bottom_center,
                content=bottom_container
            )  # Поле ввода и кнопка всегда внизу
        ],
        expand=True,
        adaptive=True

    )
