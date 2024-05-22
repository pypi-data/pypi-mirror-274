# RevampDeployer

RevampDeployer is a tool for managing and automating the deployment process of applications to remote servers.

## Installation

You can install RevampDeployer via pip:

```bash
pip install revampdeployer
```

## Usage

After installing RevampDeployer, you can use it from the command line to deploy your application to remote servers.

Example usage:

```bash
revampdeployer --config config.py
```

Here, `config.py` is the configuration file containing connection parameters to the servers and deployment settings. Please make sure your configuration file has the correct format and content.

## Configuration File (config.py)

Example `config.py` configuration file:

```python
servers = {
    "server1": {
        "address": "192.168.1.1",
        "username": "root",
        "password": "password1"
    },
    "server2": {
        "address": "192.168.1.2",
        "username": "admin",
        "password": "password2"
    },
    # Other servers...
}

local_scripts_dir = "local_scripts/"  # Директория локальных скриптов
scripts_dir = "scripts/"  # Директория скриптов для выполнения на сервере
input_dir = "input/"  # Директория с файлами для отправки на сервер
output_dir = "output/"  # Директория для размещения файлов на сервере
scripts_dir_deploy = "deploy_scripts/"  # Директория скриптов для пост-деплой конфигурации
```

This file should contain a list of servers, script directories, input and output directories, etc. Make sure all parameters are correct and match your environment.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for additional information.