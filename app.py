import os
import time
import subprocess
import json
from tqdm import tqdm

# Конфигурация
REPO_URL = 'https://github.com/globenvi/cwim-core-tgbt.git'  # URL вашего репозитория
LOCAL_REPO_PATH = os.path.join(os.getenv('HOME', '/tmp'), 'cwim-core-tgbt')  # Локальный путь для клонирования
CHECK_INTERVAL = 60  # Интервал проверки новых коммитов в секундах
VERSION_FILE = os.path.join(LOCAL_REPO_PATH, 'version.txt')  # Путь к файлу версии
ROUTES_FILE = os.path.join(LOCAL_REPO_PATH, 'routes.json')  # Путь к файлу с доступом

def load_access_rules():
    """Загружает правила доступа из файла routes.json."""
    try:
        with open(ROUTES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке файла с доступом: {e}")
        return []

def check_access(user_group, required_group):
    """Проверяет, имеет ли пользователь доступ к странице."""
    return user_group == required_group

def clone_repo():
    """Клонирует репозиторий, если он еще не существует."""
    if not os.path.exists(LOCAL_REPO_PATH):
        print(f"Клонирование репозитория из {REPO_URL} в {LOCAL_REPO_PATH}...")
        try:
            subprocess.run(['git', 'clone', REPO_URL, LOCAL_REPO_PATH], check=True)
            print("Клонирование завершено.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при клонировании репозитория: {e}")
    else:
        print("Репозиторий уже клонирован.")

def update_repo():
    """Обновляет локальный репозиторий, если есть новые коммиты."""
    print("Проверка обновлений в репозитории...")
    try:
        subprocess.run(['git', '-C', LOCAL_REPO_PATH, 'pull'], check=True)
        print("Обновление завершено: новые коммиты загружены.")
        return True  # Обновления найдены
    except subprocess.CalledProcessError:
        print("Ошибка при обновлении репозитория.")
        return False  # Обновлений нет

def run_flet_app():
    """Запускает flet приложение."""
    app_path = os.path.join(LOCAL_REPO_PATH, 'app.py')
    print(f"Запуск flet приложения: {app_path}")

    # Запускаем flet приложение
    process = subprocess.Popen(['flet', '-w', app_path])
    return process

def read_version():
    """Читает текущую версию приложения из файла."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            return f.read().strip()
    return "0.0.0"  # Если файл не найден, возвращаем базовую версию

def write_version(version):
    """Записывает текущую версию приложения в файл."""
    with open(VERSION_FILE, 'w') as f:
        f.write(version)

def main():
    # Клонируем репозиторий, если он еще не существует
    clone_repo()

    # Читаем текущую версию
    current_version = read_version()
    print(f"Текущая версия приложения: {current_version}")

    # Запускаем flet приложение
    flet_process = run_flet_app()

    try:
        while True:
            if update_repo():
                # Перезапускаем приложение при обнаружении обновлений
                flet_process.terminate()  # Завершаем текущий процесс flet
                flet_process.wait()  # Ждем завершения процесса
                flet_process = run_flet_app()  # Запускаем его снова

                # Обновляем и записываем новую версию (если доступна)
                new_version = read_version()  # Или можете использовать какую-то логику для получения новой версии
                if new_version != current_version:
                    write_version(new_version)
                    print(f"Обновление версии: {new_version}")
                    current_version = new_version

            # Отображение статус-бара
            for _ in tqdm(range(CHECK_INTERVAL), desc="Ожидание проверки обновлений", ncols=80):
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nОстановка отслеживания репозитория.")
        flet_process.terminate()  # Завершаем процесс перед выходом
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        flet_process.terminate()  # Завершаем процесс при ошибке

if __name__ == "__main__":
    main()
