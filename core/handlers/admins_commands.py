from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command
from pydantic.v1 import NoneStr

from core.middlewares.is_admin import isAdmin

router = Router()

@router.message(Command("create"))
async def ban_user(message: Message):
    pass
"""Server creating"""