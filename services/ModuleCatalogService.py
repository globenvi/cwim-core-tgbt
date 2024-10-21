# services/module_catalog_service.py
import os
import subprocess
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MODULES_REPO_URL = "https://github.com/globenvi/Modules.git"

class ModuleCatalogService:
    def __init__(self, modules_path='modules'):
        self.modules_path = modules_path
        if not os.path.exists(modules_path):
            os.makedirs(modules_path)
        self.clone_repo()

    def clone_repo(self):
        """Клонируем или обновляем репозиторий с модулями"""
        if os.path.exists(self.modules_path + "/.git"):
            subprocess.run(["git", "-C", self.modules_path, "pull"], check=True)
        else:
            subprocess.run(["git", "clone", MODULES_REPO_URL, self.modules_path], check=True)

    def list_modules(self, page=1, per_page=5):
        """Получаем список модулей с пагинацией"""
        modules = [f for f in os.listdir(self.modules_path) if os.path.isdir(os.path.join(self.modules_path, f))]
        total = len(modules)
        start = (page - 1) * per_page
        end = start + per_page
        return modules[start:end], total

    def install_module(self, module_name):
        """Устанавливаем выбранный модуль"""
        # Пример инсталляции модуля - копирование файлов или выполнение скрипта
        module_path = os.path.join(self.modules_path, module_name)
        # Логика установки модуля
        return f"Модуль {module_name} установлен."

    def create_module_keyboard(self, page=1, per_page=5):
        modules, total = self.list_modules(page, per_page)
        keyboard = InlineKeyboardMarkup(row_width=1)

        for module in modules:
            keyboard.add(InlineKeyboardButton(text=module, callback_data=f"install_{module}"))

        if page > 1:
            keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))

        if (page * per_page) < total:
            keyboard.add(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page + 1}"))

        return keyboard
