from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.controllers.ModuleController import Module

class ModuleCatalogService:
    def __init__(self):
        self.module = Module()

    async def list_modules(self, page=1, per_page=5):
        """Получаем список модулей с пагинацией."""
        modules = await self.module.list_modules()
        total = len(modules)
        start = (page - 1) * per_page
        end = start + per_page
        return modules[start:end], total

    async def install_module(self, module_name):
        """Устанавливаем выбранный модуль и добавляем его в базу данных."""
        module = Module(module_name=module_name)
        await module.create_module()
        return f"Модуль {module_name} установлен."

    async def remove_module(self, module_name):
        """Удаляем выбранный модуль из базы данных."""
        module = Module(module_name=module_name)
        await module.delete_module()
        return f"Модуль {module_name} удален."

    async def create_module_keyboard(self, page=1, per_page=5):
        """Создаем клавиатуру с модулями, пагинацией, установкой и удалением."""
        modules, total = await self.list_modules(page, per_page)
        keyboard = InlineKeyboardMarkup(row_width=1)

        for module in modules:
            keyboard.add(
                InlineKeyboardButton(text=f"Установить {module['module_name']}", callback_data=f"install_{module['module_name']}"),
                InlineKeyboardButton(text=f"Удалить {module['module_name']}", callback_data=f"delete_{module['module_name']}")
            )

        if page > 1:
            keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page-1}"))

        if (page * per_page) < total:
            keyboard.add(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page+1}"))

        return keyboard
