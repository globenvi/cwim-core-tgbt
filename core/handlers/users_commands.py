import os
import json

from aiogram import Router, Bot

from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from core.utils.commands import set_commands
from core.middlewares.is_admin import isAdmin


router = Router()


#TODO###
#*Пооверка установки файлов*#
#поверка версии ядра
#проверка модулей
#проверка версии каждого модуля
#установка файловой системы
#
@router.message(Command('install'))
async def install_core_command(message: Message):
    # Load config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Check if 'modules' section exists in config.json
    if 'modules' in config:
        # Iterate through each module in the 'modules' section
        for module_name, module_info in config['modules'].items():
            # Check if the module is active
            if module_info['active']:
                # Check if all required module information keys exist
                if all(key in module_info for key in ['version', 'author', 'tg_name']):
                    # await message.answer the module information
                    await message.answer(
                        f"Предустановленный модуль: {module_name}, версия: {module_info['version']}, автор: {module_info['author']}, имя в Telegram: {module_info['tg_name']}")
                else:
                    # await message.answer a warning if any required module information keys are missing
                    await message.answer(f"Warning: Missing required information for module {module_name}")
            else:
                # await message.answer the module name if it's not active
                await message.answer(f"Модуль {module_name} не установлен")
    else:
        # await message.answer a warning if the 'modules' section does not exist in config.json
        await message.answer("Warning: 'modules' section not found in config.json")

    # Check if 'core_settings' section exists in config.json
    if 'core_settings' in config:
        # await message.answer the core_settings information
        await message.answer(f"Настройки ядра: {config['core_settings']}")
    else:
        # await message.answer a warning if the 'core_settings' section does not exist in config.json
        await message.answer("Warning: 'core_settings' section not found in config.json")

    # Check if 'admins' section exists in config.json
    if 'admins' in config:
        # Check if the 'admins' list is empty
        if not config['admins']:
            # Add the first admin to the list if it's empty
            config['admins'] = [message.from_user.id]
            await message.answer("Первый администратор добавлен в список")
        else:
            # await message.answer the list of admins if it's not empty
            await message.answer(f"Администраторы: {config['admins']}")
    else:
        # await message.answer a warning if the 'admins' section does not exist in config.json
        await message.answer("Warning: 'admins' section not found in config.json")

    # Save the updated config.json
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)


@router.message(Command('modules'), isAdmin())
async def modules_command(message: Message):
    # Load config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Check if 'modules' section exists in config.json
    if 'modules' in config:
        # Iterate through each module in the 'modules' section
        for module_name, module_info in config['modules'].items():
            # Check if the module is active
            if module_info['active']:
                # Check if all required module information keys exist
                if all(key in module_info for key in ['version', 'author', 'tg_name']):
                    # await message.answer the module information
                    await message.answer(
                        f"Module: {module_name}\nVersion: {module_info['version']}\nAuthor: {module_info['author']}\nTelegram Name: {module_info['tg_name']}")
                else:
                    # await message.answer a warning if any required module information keys are missing
                    await message.answer(f"Warning: Missing required information for module {module_name}")
            else:
                # await message.answer the module name if it's not active
                await message.answer(f"Module {module_name} is not active")
    else:
        # await message.answer a warning if the 'modules' section does not exist in config.json
        await message.answer("Warning: 'modules' section not found in config.json")
