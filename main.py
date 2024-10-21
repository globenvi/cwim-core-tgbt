import os
import importlib
import asyncio
from tqdm import tqdm
from aiogram import Bot, Dispatcher
from config_reader import settings
from core.utils.commands import set_commands
from services.UpdateService import UpdateService

update_service = UpdateService()

async def check_for_updates():
    while True:
        if update_service.config.get('auto_update', False):
            updates = update_service.get_updates()
            if updates:
                update_service.update_core()
        await asyncio.sleep(21600)  # Проверка каждые 6 часов

async def load_modules(dp: Dispatcher):
    """Загрузка всех модулей из директории modules."""
    if os.path.exists('modules'):
        module_dirs = [d for d in os.listdir('modules') if os.path.isdir(os.path.join('modules', d))]

        for module_dir in tqdm(module_dirs, desc="Loading modules"):
            try:
                # Импортируем __init__.py из каждой папки с модулем
                module = importlib.import_module(f'modules.{module_dir}')
                if hasattr(module, 'setup'):
                    module.setup()  # Запуск функции инициализации модуля (setup())
                    print(f'Module {module_dir} loaded successfully')
                else:
                    print(f'Module {module_dir} does not have a setup() function')
            except Exception as e:
                print(f'Failed to load module {module_dir}: {e}')
    else:
        print("Warning: 'modules' directory not found")


async def main():
    bot = Bot(settings.bots.bot_tokken)  # Replace with your bot token
    dp = Dispatcher()

    # Устанавливаем команды бота
    await set_commands(bot, 'start', 'Запустить бота')
    await set_commands(bot, 'profile', 'Показать профиль пользователя')

    # Получаем все файлы хендлеров в core/handlers
    handler_files = [f[:-3] for f in os.listdir('core/handlers') if f.endswith('.py')]

    # Импортируем и включаем роутеры для каждого хендлера
    for handler_file in tqdm(handler_files, desc="Loading handlers"):
        try:
            module = importlib.import_module(f'core.handlers.{handler_file}')
            if hasattr(module, 'router'):
                dp.include_routers(module.router)
                print(f'core/handlers/{handler_file} -> {handler_file}.py -> [router]')
        except Exception as e:
            print(f"Error loading handler {handler_file}: {e}")

    # Загружаем и подключаем модули
    await load_modules(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, on_startup=check_for_updates)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
