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
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Список для отображения сообщений
    messages_list = Column(scroll=True, expand=True, alignment=MainAxisAlignment.END)

    # Загрузка существующих сообщений
    existing_messages = load_messages()
    for msg in existing_messages:
        messages_list.controls.append(Text(msg, size=14, color="black", selectable=True))

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
                    [
                        input_field,
                        send_button,
                    ],
                    alignment=MainAxisAlignment.END,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.END,
            expand=True,
        )
    )

    # Фиксация поля ввода и кнопки к низу экрана
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
        messages_list.controls.append(Text(full_message, size=14, color="black", selectable=True))
        input_field.value = ""  # Очищаем поле ввода
        messages_list.scroll = True  # Прокрутка вниз
        page.update()  # Обновляем страницу
