# admin_commands.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.update_service import UpdateService
from core.middlewares.is_admin import isAdmin
from core.keyboards.inline_keyboards import get_open_web_ui_keyboard

router = Router()
update_service = UpdateService()

@router.message(Command('test'))
async def test_updates(message: Message):
    await message.reply('Ты собака')


@router.message(Command('get_updates'), isAdmin())
async def get_updates_command(message):
    updates = update_service.get_updates()
    if updates:
        await message.answer(f"Доступные обновления:\n{updates}")
    else:
        await message.answer("Обновлений нет.")


# admin_commands.py
@router.message(Command('update_core'), isAdmin())
async def update_core_command(message):
    try:
        await message.answer("Начинаем обновление...")
        update_service.update_core()
        await message.answer("Обновление завершено. Система перезапущена.")
    except Exception as e:
        await message.answer(f"Ошибка при обновлении: {e}")


# admin_commands.py
@router.message(Command('auto_update_true'), isAdmin())
async def enable_auto_update_command(message):
    update_service.set_auto_update(True)
    await message.answer("Автоматическое обновление включено.")

@router.message(Command('auto_update_false'), isAdmin())
async def disable_auto_update_command(message):
    update_service.set_auto_update(False)
    await message.answer("Автоматическое обновление выключено.")
