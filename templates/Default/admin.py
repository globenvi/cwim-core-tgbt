from flet import *

from services.DatabaseService import JSONService

def tpl_admin(page):
    def on_delete_user(e):
        user_item = e.control.data
        page.controls[1].controls.remove(user_item)
        page.update()
    db_service = JSONService()
    users = db_service.read("users")

    user_list = ListView(controls=[
        Row([
            Text(user, size=20),
            IconButton(icons.DELETE, data=user, on_click=on_delete_user)
        ]) for user in users
    ])

    page.controls.append(Column([
        Text("Административная панель", size=30),
        Text("Здесь вы можете управлять пользователями.", size=20),
        user_list
    ]))
