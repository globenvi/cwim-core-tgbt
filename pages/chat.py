import sqlite3
import flet as ft
import asyncio
import websockets
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

# Асинхронная функция для обработки сообщений
async def websocket_client(messages_list, page):
    uri = "ws://localhost:8765"  # URL вашего WebSocket-сервера
    async with websockets.connect(uri) as websocket:
        # Загрузка существующих сообщений при подключении
        existing_messages = load_messages()
        for msg in existing_messages:
            messages_list.controls.append(ft.Text(msg, size=14, color="black", selectable=True))
        page.update()

        # Бесконечный цикл для получения сообщений
        while True:
            message = await websocket.recv()
            messages_list.controls.append(ft.Text(message, size=14, color="black", selectable=True))
            messages_list.scroll = True  # Прокрутка вниз
            page.update()  # Обновляем страницу

def tpl_chat(page: ft.Page):
    page.title = "Чат"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ThemeMode.SYSTEM

    messages_list = ft.Column(scroll=True, expand=True, alignment=ft.MainAxisAlignment.END)

    # Поле для ввода сообщения
    input_field = ft.TextField(
        label="Ваше сообщение",
        multiline=False,
        width=300,
        on_submit=lambda e: send_message(input_field, messages_list)
    )

    # Кнопка отправки сообщения
    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        on_click=lambda e: send_message(input_field, messages_list)
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

    # Запускаем клиент WebSocket в фоновом режиме
    page.start_background_task(websocket_client, messages_list, page)

def send_message(input_field, messages_list):
    """Отправляет сообщение в чат."""
    message_text = input_field.value.strip()  # Получаем текст сообщения
    if message_text:  # Если текст не пустой
        name = "Гость"  # Здесь можно добавить получение имени пользователя
        full_message = f"{name}: {message_text}"

        # Отправляем сообщение на сервер WebSocket
        asyncio.run(send_to_websocket(full_message))

        # Добавляем сообщение в список
        messages_list.controls.append(ft.Text(full_message, size=14, color="black", selectable=True))
        input_field.value = ""  # Очищаем поле ввода
        messages_list.scroll = True  # Прокрутка вниз
        messages_list.update()  # Обновляем список

async def send_to_websocket(message):
    uri = "ws://localhost:8765"  # URL вашего WebSocket-сервера
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)

# Инициализация базы данных
init_db()

