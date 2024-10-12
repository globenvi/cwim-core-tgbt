import asyncio
import subprocess
import json
import betterlogging as logging

# Настраиваем логирование
logging.basic_colorized_config()

# Функция для чтения конфигурационного файла
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

async def run_bot():
    process = await asyncio.create_subprocess_exec('python', 'main.py')
    await process.wait()

async def run_web():
    process = await asyncio.create_subprocess_exec('python', 'web/main.py')
    await process.wait()

async def main():
    # Загружаем конфигурацию
    config = load_config()

    # Проверяем параметр web_ui_active
    if config['core_settings'].get('web_ui_active', False):
        print("Web UI is active, launching both bot and web interface.")
        await asyncio.gather(run_bot(), run_web())
    else:
        print("Web UI is disabled, launching only the bot.")
        await run_bot()

if __name__ == "__main__":
    asyncio.run(main())
