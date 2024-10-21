from g4f.gui import run_gui
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from core.keyboards.inline_keyboards import get_open_web_ui_keyboard

router = Router()


@router.message(Command("gpt"))
async def generate_response(message: Message):
    await message.reply(f"Web GPT started", reply_markup=get_open_web_ui_keyboard())
    run_gui()