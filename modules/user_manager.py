from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from core.middlewares.is_admin import isAdmin
from modules.um_files import database
import os
import json
import importlib

router = Router()

db = database



@router.message(CommandStart())
async def user_start_command(message: Message):
    await db.find_one("users", user_id=message.from_user.id)