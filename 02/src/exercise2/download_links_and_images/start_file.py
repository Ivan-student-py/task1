import os  # для работы с путями
import asyncio  # основа асинхронности
import aiohttp  # для асинхронных http-запросов (нужно установить)

# Функция запроса пути сохранения


class ImageDownloader:
    def __init__(self):
        # всегда строковое поле у объекта класса
        self.save_directory: str = ""
        # список кортежей ссылок и статусов
        self.results: list[tuple[str, str]] = []
        # для контроля сессии
        self.session: aiohttp.ClientSession | None = None

    def get_valid_save_directory(self) -> str:
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
                print(
                    f"Error: no permission to write to the directory '{path}'.")
                continue

            return path

    # объявление асинхронного метода run (способного вызывать асинх функции)
    async def run(self) -> None:
        # вызов синхронного метода и его сохранение в поле объекта
        self.save_directory = self.get_valid_save_directory()
        print(f"Selectef directory: {self.save_directory}")

        # создание асинхронной http-сессии:
        # создание асинх контекстного менеджера для http-сессии,
        # с закрытием после завершения блока
        async with aiohttp.ClientSession() as session:
            self.session = session
            # запуск асинх цикла ввода URL
            # и загрузки изображений с ожиданием завершения
            await self._input_loop()

        # вызов метода вывода итоговой таблицы
        await self._print_summary()

    # метод управления вводом URL от пользователя
    async def _input_loop(self) -> None:
        # получение основного цикла событий asyncio, управляющего асинх задачами
        loop = asyncio.get_event_loop()
        # список асинх задач
        tasks = []

        while True:
            # выполнение синх функ инпут в пуле потоков по умолчанию
            # чтобы не блокировать event loop
            url = await loop.run_in_executor(
                None, input, "Enter image URL (empty to finish): ")
            url = url.strip()

            if not url:
                break


if __name__ == "__main__":
    downloader = ImageDownloader()
    asyncio.run(downloader.run())
