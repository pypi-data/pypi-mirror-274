#!/usr/bin/env python

import importlib.resources as pkg_resources
import os
import asyncio
import asyncssh
import sys
import tarfile
from loguru import logger
from tqdm import tqdm

# Функция для загрузки содержимого файла config.py из текущей директории
def load_config():
    try:
        with open("config.py") as f:
            code = f.read()
        config_module = type(sys)("config")
        exec(code, config_module.__dict__)
        return config_module
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

# Загружаем конфигурацию из файла config.py
config = load_config()

async def connect_to_server(remote_host, username, password, port=22):
    # Подключение к серверу
    try:
        conn = await asyncssh.connect(remote_host, port=port, username=username,
                                      password=password, known_hosts=None)
        logger.success(f"Successfully connected to {remote_host}.")
        await print_os_info(conn)  # Вызываем функцию для вывода информации об ОС
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to {remote_host}: {e}")
        return None


async def print_os_info(conn):
    # Вывод информации об операционной системе
    try:
        result = await conn.run('uname -a')
        logger.info(f"Operating System Information:\n{result.stdout.strip()}")
    except Exception as e:
        logger.error(f"An error occurred while getting OS info: {e}")


async def execute_script(conn, script_path):
    # Выполнение скрипта на удаленном сервере
    try:
        async with conn:
            result = await conn.run(f'bash {script_path}', check=True)
            logger.success(f"Script {script_path} executed successfully.")
    except Exception as e:
        logger.error(f"An error occurred while executing script {script_path}: {e}")
        sys.exit(1)


async def install_configure_environment(conn, scripts_dir):
    # Установка и настройка окружения на удаленном сервере
    scripts = os.listdir(scripts_dir)
    if not scripts:
        logger.info("No scripts found in the specified directory.")
        return

    tasks = [execute_script(conn, os.path.join(scripts_dir, script)) for script in scripts]

    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Installing & Configuring Environment"):
        await f


async def send_files_to_server(conn, output_dir, input_dir):
    try:
        async with conn.start_sftp_client() as sftp:
            remote_files = await sftp.listdir(output_dir)
            logger.info(f"Remote files in {output_dir}: {remote_files}")

            # Архивируем файлы для передачи
            tar_path = 'files.tar'
            with tarfile.open(tar_path, "w") as tar:
                tar.add(input_dir, arcname=os.path.basename(input_dir))

            # Отправляем архив на сервер
            await sftp.put(tar_path, os.path.join(output_dir, tar_path))

            # Разархивируем архив на сервере
            result = await conn.run(f'tar -xf {os.path.join(output_dir, tar_path)} -C {output_dir}', check=True)
            logger.success("Files extracted on the server successfully.")

            # Удаляем архив
            os.remove(tar_path)
            await conn.run(f'rm {os.path.join(output_dir, tar_path)}', check=True)

        logger.success("Files sent to the server successfully.")
    except Exception as e:
        logger.error(f"An error occurred while sending files to the server: {e}")
        sys.exit(1)


async def post_deploy_configuration(conn, scripts_dir_deploy):
    scripts = os.listdir(scripts_dir_deploy)
    if not scripts:
        logger.info("No scripts found in the specified directory.")
        return

    tasks = [execute_script(conn, os.path.join(scripts_dir_deploy, script)) for script in scripts]

    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Post-deployment Configuration"):
        await f


async def deploy_to_server(remote_host, port, username, password, scripts_dir, input_dir, output_dir, scripts_dir_deploy):
    # Подключение к серверу
    conn = await connect_to_server(remote_host, port, username, password)
    if conn is None:
        return

    # Установка и настройка окружения на удаленном сервере
    await install_configure_environment(conn, scripts_dir)

    # Отправка файлов на сервер
    await send_files_to_server(conn, output_dir, input_dir)

    # Настройка после развертывания на сервере
    await post_deploy_configuration(conn, scripts_dir_deploy)

    # Закрыть соединение
    conn.close()


def parse_server_string(server_string):
    # Парсинг строки подключения в формате 192.168.1.0@root:password
    try:
        address, credentials = server_string.split('@')
        username, password = credentials.split(':')
        return address, username, password
    except ValueError:
        raise ValueError("Server string must be in the format 192.168.1.0@root:password")


def main():
    # Получаем конфигурации из config.py
    servers = [parse_server_string(server) for server in config.servers]
    scripts_dir = config.scripts_dir
    input_dir = config.input_dir
    output_dir = config.output_dir
    scripts_dir_deploy = config.scripts_dir_deploy

    # Создаем цикл событий для выполнения асинхронных функций
    loop = asyncio.get_event_loop()

    tasks = [deploy_to_server(remote_host, 22, username, password, scripts_dir, input_dir, output_dir, scripts_dir_deploy)
             for remote_host, username, password in servers]

    loop.run_until_complete(asyncio.gather(*tasks))

    # Завершить цикл событий
    loop.close()


if __name__ == '__main__':
    main()
