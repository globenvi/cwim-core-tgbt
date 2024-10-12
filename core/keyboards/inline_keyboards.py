from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, InlineQuery


profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить Аватар", callback_data="change_name")
        ],
        [
            InlineKeyboardButton(text="Изменить Ник", callback_data="change_avatar"),
            InlineKeyboardButton(text="Изменить Подпись", callback_data="change_signature")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back_to_main")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2,
    selective=False,  # optional, defaults to False
)

