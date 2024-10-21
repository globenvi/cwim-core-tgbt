from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

def setup_handlers(router: Router):
    """Функция для регистрации всех хендлеров этого модуля."""
    @router.message(Command('test'))
    async def custom_command_handler(message: Message):
        await message.answer("Это команда из модуля!")
