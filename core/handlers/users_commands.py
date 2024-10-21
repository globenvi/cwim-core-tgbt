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
    user_data = await user.read_user()

    if not user_data:
        await message.reply(f'Добро пожаловать {message.from_user.username}\n'
                            f'Пожалуйста, ознакомься с правилами проекта! /rules', parse_mode="HTML")
        await user.create('user', user_data)
    else:
        await message.reply(f'С возвраением!, {message.from_user.username}!')