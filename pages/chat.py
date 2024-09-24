from flet import *

# Хранилище сообщений
messages = []

def tpl_chat(page: Page):
    page.title = "Онлайн Чат"

    # Запрос имени пользователя и сохранение в сессию
    if not page.session.get("username"):
        username_input = TextField(label="Введите ваше имя", width=300)
        submit_button = ElevatedButton(
            "Подтвердить",
            on_click=lambda e: set_username(page, username_input.value),
            width=100
        )

        page.add(
            Column(
                [
                    username_input,
                    submit_button,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()
    else:
        username = page.session.get("username")

        # Поле для ввода нового сообщения
        message_input = TextField(label="Введите сообщение", width=300, multiline=True)

        # Кнопка отправки сообщения с иконкой
        send_button = IconButton(
            icon=icons.SEND,
            on_click=lambda e: send_message(page, username, message_input.value),
            tooltip="Отправить",
            icon_size=30  # Размер иконки
        )

        # Список для отображения сообщений
        message_list = Column(spacing=10)

        # Добавляем элементы на страницу
        page.add(
            Column(
                [
                    message_list,
                    Row(
                        [message_input, send_button],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=20
            )
        )

        # Функция для отображения сообщений
        def display_messages():
            message_list.controls.clear()
            for msg in messages:
                msg_text = Text(f"{msg['username']}: {msg['text']}", size=16)
                if msg['username'] == username:  # Удалять может только отправитель
                    delete_button = IconButton(
                        icon=icons.DELETE,
                        on_click=lambda e, m=msg: delete_message(m),
                        tooltip="Удалить сообщение"
                    )
                    message_list.controls.append(Row([msg_text, delete_button], alignment=MainAxisAlignment.SPACE_BETWEEN))
                else:
                    message_list.controls.append(msg_text)
            page.update()

        # Функция для отправки сообщения
        def send_message(page, username, text):
            if text.strip():
                messages.append({"username": username, "text": text})
                message_input.value = ""  # Очищаем поле ввода
                display_messages()  # Обновляем список сообщений

        # Функция для удаления сообщения
        def delete_message(msg):
            messages.remove(msg)
            display_messages()  # Обновляем список сообщений

        # Запуск функции обновления сообщений в реальном времени
        def update_messages():
            display_messages()
            page.update()
            page.timer(1, update_messages)  # Обновление каждую секунду

        update_messages()  # Начальное отображение сообщений

def set_username(page: Page, username: str):
    """Устанавливает имя пользователя и обновляет страницу."""
    if username.strip():
        page.session.set("username", username)
        page.controls.clear()  # Очищаем экран
        tpl_chat(page)  # Перезагружаем чат
    else:
        page.snack_bar = SnackBar(Text("Имя не может быть пустым!", color=colors.WHITE), bgcolor=colors.RED)
        page.snack_bar.open = True
        page.update()

# Запуск Flet
if __name__ == "__main__":
    app(target=tpl_chat, view=AppView.WEB_BROWSER)
