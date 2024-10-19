import asyncio
import subprocess
import json

import subprocess
import requests
import time

# Переменная для хранения authtoken
NGROK_AUTH_TOKEN = '2mW2Z5tLviLYnvm06ocNzsXFPhV_59UFWBgh3eu1G91DeqoSw'
ngrok_url = ""

# Функция для авторизации ngrok с использованием токена
def authenticate_ngrok(token):
    result = subprocess.run(['ngrok', 'authtoken', token], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка при авторизации: {result.stderr}")
        return False
    return True

# Функция для запуска ngrok на указанном порту
def start_ngrok(port):
    process = subprocess.Popen(['ngrok', 'http', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Ожидание запуска туннеля
    return process

# Функция для получения публичного URL активного туннеля
def get_ngrok_public_url():
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        response.raise_for_status()
        data = response.json()
        return data['tunnels'][0]['public_url']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе URL туннеля: {e}")
        return None

# Авторизация ngrok
if authenticate_ngrok(NGROK_AUTH_TOKEN):
    # Запуск туннеля на порту 5000
    process = start_ngrok(5000)

    # Получение публичного URL туннеля
    public_url = get_ngrok_public_url()
    if not public_url:
        print("Авторизация не удалась!")
    else:
        ngrok_url = public_url



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
