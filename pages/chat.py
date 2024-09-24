import json
import os
from flet import *

DATA_FILE = './cwim-core-tgbt/datafiles/chat_data.json'

# Проверка наличия файла и создание, если не существует
def check_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)  # Инициализируем пустым массивом
    else:
        # Проверяем, что содержимое файла является корректным JSON
        with open(DATA_FILE, 'r') as f:
            try:
                json.load(f)
            except json.JSONDecodeError:
                # Если содержимое некорректное, переинициализируем
                with open(DATA_FILE, 'w') as f:
                    json.dump([], f)

# Загрузка сообщений из JSON файла
def load_messages():
    check_data_file()
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Ошибка загрузки сообщений: неверный формат данных.")
        return []  # Возвращаем пустой список в случае ошибки

# Сохранение сообщений в JSON файл
def save_message(message):
    messages = load_messages()
    messages.append(message)
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

# Удаление сообщения по индексу
def delete_message(index):
    messages = load_messages()
    if 0 <= index < len(messages):
        messages.pop(index)
        with open(DATA_FILE, 'w') as f:
            json.dump(messages, f, indent=4)

def tpl_chat(page: Page):
    page.title = "Чат"

    # Инициализация элементов страницы
    messages_list = Column()
    input_field = TextField(label="Введите сообщение...", width=300)
    send_button = IconButton(icon=icons.SEND, on_click=lambda e: send_message(input_field, messages_list, page))

    # Загрузка сообщений при старте
    load_existing_messages(messages_list)

    # Добавляем элементы на страницу
    page.add(
        Column(
            [
                messages_list,
                Row([input_field, send_button]),
            ],
            alignment=MainAxisAlignment.START,
        )
    )

    # Обновление сообщений в реальном времени
    def update_messages():
        messages_list.controls.clear()
        load_existing_messages(messages_list)
        page.update()

    page.on_interval = update_messages

def load_existing_messages(messages_list):
    messages = load_messages()
    for index, msg in enumerate(messages):
        msg_control = Row(
            [
                Text(f"{msg['name']}: {msg['message']}"),
                IconButton(icon=icons.DELETE, on_click=lambda e, idx=index: delete_message_action(idx, messages_list)),
            ],
            alignment=MainAxisAlignment.START,
        )
        messages_list.controls.append(msg_control)

def send_message(input_field, messages_list, page):
    name = page.session.get("user_name", "Гость")  # Получаем имя пользователя из сессии
    message = input_field.value.strip()
    if message:
        save_message({"name": name, "message": message})
        input_field.value = ""  # Очищаем поле ввода
        input_field.update()

def delete_message_action(index, messages_list):
    delete_message(index)
    messages_list.controls.clear()
    load_existing_messages(messages_list)

# Запуск Flet
if __name__ == "__main__":
    import flet as ft
    ft.app(target=tpl_chat, view=ft.AppView.WEB_BROWSER)
