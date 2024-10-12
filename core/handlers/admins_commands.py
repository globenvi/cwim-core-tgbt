from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command
from pydantic.v1 import NoneStr

from core.middlewares.is_admin import isAdmin

router = Router()

@router.message(Command("ban"), isAdmin())
async def ban_user(message: Message):
    await message.reply(f"User USER has been banned.")