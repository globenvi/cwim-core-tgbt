import json
from flet import *


# Функция для загрузки существующих сообщений из файла
def load_messages():
    try:
        with open('./cwim-core-tgbt/datafiles/messages.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Возвращаем пустой список, если файл не найден или не может быть прочитан


# Функция для сохранения сообщения в файл
def save_message(message):
    messages = load_messages()
    messages.append(message)
    with open('./cwim-core-tgbt/datafiles/messages.json', 'w') as f:
        json.dump(messages, f)


def tpl_chat(page: Page):
    page.title = "Чат"

    # Список для отображения сообщений
    messages_list = Column()

    # Загрузка существующих сообщений
    existing_messages = load_messages()
    for msg in existing_messages:
        messages_list.add(Text(msg))

    # Поле для ввода сообщения
    input_field = TextField(
        label="Ваше сообщение",
        multiline=False,
        width=300,
        on_submit=lambda e: send_message(input_field, messages_list, page)
    )

    # Кнопка отправки сообщения
    send_button = IconButton(
        icon=icons.SEND,
        on_click=lambda e: send_message(input_field, messages_list, page)
    )

    # Добавляем элементы на страницу
    page.add(
        Column(
            [
                messages_list,
                Row(
                    [input_field, send_button],
                    alignment=MainAxisAlignment.CENTER
                )
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )

    page.update()


def send_message(input_field, messages_list, page):
    """Отправляет сообщение в чат."""
    message_text = input_field.value.strip()  # Получаем текст сообщения
    if message_text:  # Если текст не пустой
        # Получаем имя пользователя из сессии, установив "Гость" как значение по умолчанию
        name = page.session.get("user_name") or "Гость"
        full_message = f"{name}: {message_text}"

        # Сохраняем сообщение в файл
        save_message(full_message)

        # Добавляем сообщение в список
        messages_list.add(Text(full_message))
        input_field.value = ""  # Очищаем поле ввода
        page.update()  # Обновляем страницу
