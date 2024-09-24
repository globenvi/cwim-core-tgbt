import sqlite3
import flet as ft
from flet_core import ThemeMode


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

async def update_messages(page, messages_list):
    while True:
        await asyncio.sleep(2)  # Пауза между обновлениями
        new_messages = load_messages()
        messages_list.controls.clear()  # Очищаем список перед обновлением
        for msg in new_messages:
            messages_list.controls.append(ft.Text(msg, size=14, color="black", selectable=True))
        page.update()  # Обновляем страницу

def tpl_chat(page: ft.Page):
    page.title = "Чат"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ThemeMode.SYSTEM
    # Список для отображения сообщений
    messages_list = ft.Column(scroll=True, expand=True, alignment=ft.MainAxisAlignment.END)

    # Загрузка существующих сообщений
    existing_messages = load_messages()
    for msg in existing_messages:
        messages_list.controls.append(ft.Text(msg, size=14, color="black", selectable=True))

    # Поле для ввода сообщения
    input_field = ft.TextField(
        label="Ваше сообщение",
        multiline=False,
        width=300,
        on_submit=lambda e: send_message(input_field, messages_list, page)
    )

    # Кнопка отправки сообщения
    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        on_click=lambda e: send_message(input_field, messages_list, page)
    )

    # Добавляем элементы на страницу
    page.add(
        ft.Column(
            [
                messages_list,
                ft.Row(
                    [
                        input_field,
                        send_button,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )
    )

    # Запускаем асинхронную задачу для обновления сообщений с использованием Flet
    page.start_background_task(update_messages, page, messages_list)

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
        messages_list.controls.append(ft.Text(full_message, size=14, color="black", selectable=True))
        input_field.value = ""  # Очищаем поле ввода
        messages_list.scroll = True  # Прокрутка вниз
        page.update()  # Обновляем страницу

# Инициализация базы данных
init_db()