# admin_commands.py
from aiogram import Router
from aiogram.filters import Command
from services.update_service import UpdateService
from core.middlewares.is_admin import IsAdmin

router = Router()
update_service = UpdateService()

@router.message(Command('get_updates'), IsAdmin())
async def get_updates_command(message):
    updates = update_service.get_updates()
    if updates:
        await message.answer(f"Доступные обновления:\n{updates}")
    else:
        await message.answer("Обновлений нет.")
