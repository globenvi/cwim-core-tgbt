from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command

from core.middlewares.is_admin import isAdmin
from services.DatabaseService import JSONService
from core.controllers.UserController import User

router = Router()

@router.message(Command('start'))
async def start_bot(message: Message):
    user = User(message.from_user)

    await user.init()

    user_data = message.from_user
    await user.create_user()
