from aiogram import Router
from .handlers import setup_handlers

router = Router()

def setup():
    """Настройка модуля."""
    setup_handlers(router)

    # Можно добавить другие функции инициализации модуля при необходимости
