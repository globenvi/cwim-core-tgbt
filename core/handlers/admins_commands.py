# admin_commands.py
from aiogram import Router
from aiogram.filters import Command

from services.update_service import UpdateService
from core.middlewares.is_admin import IsAdmin
from core.keyboards.inline_keyboards import get_open_web_ui_keyboard

from init import ngrok_url

router = Router()
update_service = UpdateService()


@router.message(Command('test_ui'), IsAdmin())
async def test_ui_command(message):
    await message.answer("Тестирование Flet UI", reply_markup=get_open_web_ui_keyboard(message.from_user.id))
    await message.answer(f'DBG ngrok url: {ngrok_url}')

@router.message(Command('get_updates'), IsAdmin())
async def get_updates_command(message):
    updates = update_service.get_updates()
    if updates:
        await message.answer(f"Доступные обновления:\n{updates}")
    else:
        await message.answer("Обновлений нет.")
