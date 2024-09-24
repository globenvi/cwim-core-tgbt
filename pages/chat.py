import flet as ft
import sqlite3


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Неизвестно"  # или любое другое значение по умолчанию

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def init_db():
    """Инициализация базы данных и создание таблицы для сообщений."""
    conn = sqlite3.connect('chat_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_message(user_name: str, text: str):
    """Сохранение сообщения в базе данных."""
    conn = sqlite3.connect('chat_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (user_name, text) VALUES (?, ?)', (user_name, text))
    conn.commit()
    conn.close()


def tpl_chat(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "Чат Flet"

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Имя не может быть пустым!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} присоединился к чату.",
                    message_type="login_message",
                )
            )
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            message_text = new_message.value
            user_name = page.session.get("user_name")
            save_message(user_name, message_text)  # Сохраняем сообщение в БД
            page.pubsub.send_all(
                Message(
                    user_name=user_name,
                    text=message_text,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
            ft.notification(f"Новое сообщение от {message.user_name}")  # Уведомление о новом сообщении
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            ft.notification(f"Пользователь {message.user_name} присоединился к чату")  # Уведомление о новом пользователе
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # Диалог для ввода имени пользователя
    join_user_name = ft.TextField(
        label="Введите ваше имя для присоединения к чату",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Добро пожаловать!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Присоединиться к чату", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Сообщения чата
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # Форма ввода нового сообщения
    new_message = ft.TextField(
        hint_text="Напишите сообщение...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Добавление элементов на страницу
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Отправить сообщение",
                    on_click=send_message_click,
                ),
            ]
        ),
    )


# Инициализация базы данных
init_db()
