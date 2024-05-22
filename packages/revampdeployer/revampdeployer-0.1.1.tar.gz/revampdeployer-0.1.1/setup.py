from setuptools import setup, find_packages

# Читаем содержимое файла README.md
with open("ReadMe.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="revampdeployer",
    version="0.1.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "revampdeployer = revampdeployer.__main__:main"
        ]
    },
    # Добавляем описание пакета из README.md
    long_description=long_description,
    long_description_content_type="text/markdown",
)