import flet as ft

# Глобальные переменные для хранения сообщений и имени пользователя
messages = []
username = ""

def main(page: ft.Page):
    global username

    def open_popup(e):
        # Открытие всплывающего окна для ввода имени пользователя
        popup = ft.AlertDialog(
            title="Введите ваше имя",
            content=ft.Column(
                [
                    ft.TextField(label="Имя пользователя", on_submit=on_username_submit),
                    ft.Row(
                        [
                            ft.ElevatedButton("OK", on_click=on_username_submit),
                            ft.ElevatedButton("Отмена", on_click=lambda e: popup.close()),
                        ]
                    ),
                ]
            ),
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def on_username_submit(e):
        nonlocal username
        username = e.control.value
        page.dialog.close()
        page.update()

    def send_message(e):
        global messages
        message_text = message_input.value.strip()
        if message_text:
            messages.append(f"{username}: {message_text}")
            message_input.value = ""
            update_chat()
            page.update()

    def update_chat():
        chat_area.controls.append(ft.Text("\n".join(messages), size=12))
        chat_area.scroll = True

    # Инициализация элементов интерфейса
    page.title = "Realtime Online Chat"
    page.vertical_alignment = ft.MainAxisAlignment.START

    chat_area = ft.Column(scroll=True)
    message_input = ft.TextField(label="Ваше сообщение", on_submit=send_message)

    # Кнопка для открытия окна ввода имени
    start_button = ft.ElevatedButton("Начать чат", on_click=open_popup)

    page.add(start_button, chat_area, message_input)
