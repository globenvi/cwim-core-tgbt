# services/update_service.py
import os
import subprocess
import json

class UpdateService:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        """Загружаем конфигурацию из config.json"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        """Сохраняем конфигурацию в config.json"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_updates(self):
        """Проверяем, есть ли новые коммиты на удалённой ветке."""
        try:
            # Сравниваем локальную ветку с удалённой
            result = subprocess.run(
                ["git", "fetch"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Теперь проверяем новые коммиты, которых нет локально
            result = subprocess.run(
                ["git", "log", "HEAD..origin/main", "--oneline"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.stdout:
                return result.stdout  # Возвращаем список новых коммитов
            else:
                return "Обновлений нет."

        except subprocess.CalledProcessError as e:
            return f"Ошибка при проверке обновлений: {e}"

    def update_core(self):
        """Обновляем проект с GitHub и перезапускаем"""
        subprocess.run(["git", "pull"], check=True)
        self.restart_system()

    def set_auto_update(self, enabled: bool):
        """Включаем или выключаем автообновление в конфиге"""
        self.config['auto_update'] = enabled
        self.save_config()

    def restart_system(self):
        """Перезапуск бота, Ngrok и Flet UI"""
        os.system("pkill -f 'python init.py'")
        subprocess.run(["python", "init.py"])

