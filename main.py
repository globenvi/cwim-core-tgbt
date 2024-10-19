# Import necessary modules
import os
import importlib
import asyncio
from tqdm import tqdm

from aiogram import Bot, Dispatcher

from config_reader import settings
from core.utils.commands import set_commands

async def main():
    bot = Bot(settings.bots.bot_tokken)  # Replace with your bot token
    dp = Dispatcher()

    await set_commands(bot, 'start', 'Запустить бота')
    await set_commands(bot, 'profile', 'Показать профиль пользователя')

    # Get all .py files in the core/handlers and modules directories
    handler_files = [f[:-3] for f in os.listdir('core/handlers') if f.endswith('.py')]

    # Handle the case where 'modules' directory might not exist
    if os.path.exists('modules'):
        module_files = [f[:-3] for f in os.listdir('modules') if f.endswith('.py')]
    else:
        module_files = []
        print("Warning: 'modules' directory not found")

    # Import and include routers from each handler file
    for handler_file in tqdm(handler_files, desc="Loading handlers"):
        module = importlib.import_module(f'core.handlers.{handler_file}')
        if hasattr(module, 'router'):
            dp.include_routers(module.router)
            print(f'core/handlers/{handler_file} -> {handler_file}.py -> [router]')

    if os.path.exists('modules'):
        module_files = [f[:-3] for f in os.listdir('modules') if f.endswith('.py')]
        for module_file in tqdm(module_files, desc="Loading modules"):
            module = importlib.import_module(f'modules.{module_file}')
            if hasattr(module, 'router'):
                dp.include_routers(module.router)
                print(f'modules/{module_file} -> {module_file}.py -> [router]')
    else:
        print("Warning: 'modules' directory not found")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())