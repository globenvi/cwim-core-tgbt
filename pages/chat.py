import pymongo
from flet import *

# Настройка соединения с MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chat_database"]
messages_collection = db["messages"]

# Функция для загрузки существующих сообщений из MongoDB
def load_messages():
    return [msg["text"] for msg in messages_collection.find()]

# Функция для сохранения сообщения в MongoDB
def save_message(message):
    messages_collection.insert_one({"text": message})

def tpl_chat(page: Page):
    page.title = "Чат"

    # Список для отображения сообщений
    messages_list = Column()

    # Загрузка существующих сообщений
    existing_messages = load_messages()
    for msg in existing_messages:
        messages_list.controls.append(Text(msg))

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

        # Сохраняем сообщение в MongoDB
        save_message(full_message)

        # Добавляем сообщение в список
        messages_list.controls.append(Text(full_message))
        input_field.value = ""  # Очищаем поле ввода
        page.update()  # Обновляем страницу

# Запуск приложения
ft.app(target=tpl_chat)
