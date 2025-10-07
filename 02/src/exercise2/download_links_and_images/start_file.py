import os  # для работы с путями
import asyncio  # основа асинхронности
import aiohttp  # для асинхронных http-запросов (нужно установить)

# Функция запроса пути сохранения


def get_valid_save_directory() -> str:
    while True:
        path = input("Input path for saving img: ").strip()
        if not path:
            print("Path can't be empty. Try again.")
            continue

        if not os.path.isdir(path):
            print(f"Error: path '{path}' is not an existing directory.")
            continue

        # проверка прав на запись
        if not os.access(path, os.W_OK):
            print(f"Error: no permission to write to the directory '{path}'.")
            continue

        return path


if __name__ == "__main__":
    save_dir = get_valid_save_directory()
    print(f"Chosen directory: {save_dir}")
