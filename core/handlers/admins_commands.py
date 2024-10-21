# admin_commands.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from services.UpdateService import UpdateService
from core.middlewares.is_admin import isAdmin
from core.middlewares.is_private import isPrivate
from services.ModuleCatalogService import ModuleCatalogService

module_catalog_service = ModuleCatalogService()
router = Router()
update_service = UpdateService()

@router.message(Command('modules'), isAdmin(), isPrivate())
async def show_modules_catalog(message: Message):
    keyboard = await module_catalog_service.create_module_keyboard(page=1)
    await message.answer("Каталог модулей:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("install_"))
async def install_module(callback_query: CallbackQuery):
    module_name = callback_query.data.split("_")[1]
    result = await module_catalog_service.install_module(module_name)
    await callback_query.message.answer(result)

@router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_module(callback_query: CallbackQuery):
    module_name = callback_query.data.split("_")[1]
    result = await module_catalog_service.remove_module(module_name)
    await callback_query.message.answer(result)

@router.callback_query(lambda c: c.data.startswith("page_"))
async def paginate_modules(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    keyboard = await module_catalog_service.create_module_keyboard(page=page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

@router.message(Command('get_updates'), isAdmin(), isPrivate())
async def get_updates_command(message):
    updates = update_service.get_updates()
    if updates:
        await message.answer(f"Доступные обновления:\n{updates}")
    else:
        await message.answer("Обновлений нет.")

# admin_commands.py
@router.message(Command('update_core'), isAdmin(), isPrivate())
async def update_core_command(message):
    try:
        await message.answer("Начинаем обновление...")
        update_service.update_core()
        await message.answer("Обновление завершено. Система перезапущена.")
    except Exception as e:
        await message.answer(f"Ошибка при обновлении: {e}")


# admin_commands.py
@router.message(Command('auto_update_true'), isAdmin(), isPrivate())
async def enable_auto_update_command(message):
    update_service.set_auto_update(True)
    await message.answer("Автоматическое обновление включено.")

@router.message(Command('auto_update_false'), isAdmin(), isPrivate())
async def disable_auto_update_command(message):
    update_service.set_auto_update(False)
    await message.answer("Автоматическое обновление выключено.")
