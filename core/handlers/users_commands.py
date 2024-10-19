import os
import subprocess
import urllib.request
import zipfile
from tqdm import tqdm
import time


def download_steamcmd(steamcmd_dir):
    """Функция для автоматической загрузки SteamCMD"""
    if not os.path.exists(steamcmd_dir):
        os.makedirs(steamcmd_dir)

    steamcmd_zip_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    local_zip_path = os.path.join(steamcmd_dir, "steamcmd.zip")
    steamcmd_exe_path = os.path.join(steamcmd_dir, "steamcmd.exe")

    if not os.path.exists(steamcmd_exe_path):
        print("Скачивание SteamCMD...")

        # Скачиваем SteamCMD
        urllib.request.urlretrieve(steamcmd_zip_url, local_zip_path)

        # Распаковываем архив
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            zip_ref.extractall(steamcmd_dir)

        # Удаляем архив после распаковки
        os.remove(local_zip_path)
        print("SteamCMD успешно скачан и установлен.")
    else:
        print("SteamCMD уже установлен.")

    return steamcmd_exe_path


def install_css_server(steamcmd_dir, steamcmd_exe):
    """Функция для установки сервера CSS через SteamCMD с прогрессом"""
    install_dir = os.path.join(steamcmd_dir, 'steamapps', 'common', 'Counter-Strike Source Dedicated Server')

    if os.path.exists(os.path.join(install_dir, 'srcds.exe')):
        print("Сервер уже установлен.")
        return True  # Сервер уже существует, возвращаем True

    steamcmd_command = [
        steamcmd_exe,
        '+login', 'anonymous',
        '+force_install_dir', install_dir,
        '+app_update', '232330',
        'validate',
        '+quit'
    ]

    tqdm_desc = "Установка сервера CS:S"
    with tqdm(total=100, desc=tqdm_desc, ncols=100) as pbar:
        process = subprocess.Popen(steamcmd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   bufsize=1)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                tqdm_output_processing(output.strip(), pbar)
            time.sleep(0.1)

        process.communicate()

    return False  # Сервер был только что установлен, возвращаем False


def tqdm_output_processing(output, pbar):
    """Обновляем прогресс бар на основе вывода SteamCMD"""
    if "downloading" in output.lower() or "download complete" in output.lower():
        pbar.update(1)
    elif "Success!" in output:
        pbar.update(pbar.total - pbar.n)
    print(output)  # Выводим строку для отладки


def run_css_server(steamcmd_dir):
    """Функция для запуска сервера CS:S"""
    install_dir = os.path.join(steamcmd_dir, 'steamapps', 'common', 'Counter-Strike Source Dedicated Server')
    srcds_exe = os.path.join(install_dir, 'srcds.exe')  # Для Windows

    if not os.path.exists(srcds_exe):
        print(f"srcds.exe не найден в {install_dir}. Убедитесь, что сервер установлен правильно.")
        return

    server_command = [
        srcds_exe,
        '-game', 'cstrike',
        '-console',
        '+maxplayers', '16',
        '+map', 'de_dust2'
    ]

    tqdm_desc = "Запуск сервера CS:S"
    with tqdm(total=1, desc=tqdm_desc, ncols=100) as pbar:
        subprocess.Popen(server_command)
        pbar.update(1)


if __name__ == "__main__":
    # Путь для установки SteamCMD
    steamcmd_directory = r'steamcmd'  # Измените на нужный путь для вашей системы

    # Шаг 1: Скачивание и установка SteamCMD
    steamcmd_path = download_steamcmd(steamcmd_directory)

    # Шаг 2: Проверка и установка сервера CS:S с логированием (если нужно)
    server_exists = install_css_server(steamcmd_directory, steamcmd_path)

    # Шаг 3: Запуск сервера CS:S
    if server_exists:
        print("Сервер уже установлен. Запуск сервера...")
    run_css_server(steamcmd_directory)
