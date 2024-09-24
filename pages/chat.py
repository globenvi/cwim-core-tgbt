import sqlite3
from flet import *

# Функция для подключения к базе данных SQLite и создания таблицы, если она не существует
def init_db():
    conn = sqlite3.connect('chat_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для загрузки существующих сообщений из базы данных
def load_messages():
    conn = sqlite3.connect('chat_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM messages')
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    return messages

# Функция для сохранения сообщения в базу данных
def save_message(message):
    conn = sqlite3.connect('chat_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (text) VALUES (?)', (message,))
    conn.commit()
    conn.close()

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
                    alignment=MainAxisAlignment.END,  # Здесь используем только alignment
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

        # Сохраняем сообщение в базе данных
        save_message(full_message)

        # Добавляем сообщение в список
        messages_list.controls.append(Text(full_message, size=14, color="black", selectable=True))
        input_field.value = ""  # Очищаем поле ввода
        messages_list.scroll = True  # Прокрутка вниз
        page.update()  # Обновляем страницу

# Инициализация базы данных
init_db()

