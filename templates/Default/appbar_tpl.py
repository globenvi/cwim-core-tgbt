from flet import *

def appbar_tpl(page: Page):

    def check_item_clicked(e):
        e.control.checked = not e.control.clicked
        page.update()


    app_bar = AppBar(
        # leading=Icon(icons.PALLETE),
        leading_width=40,
        title=page.title,
        center_title=False,
        bgcolor=colors.AMBER,
        actions=[

        ]
    )

    page.controls.append(app_bar)