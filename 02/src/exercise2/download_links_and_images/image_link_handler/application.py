import asyncio
import aiohttp
from typing import List, Tuple
from .path_validator import PathValidator
from .image_downloader import ImageDownloader
from .summary_printer import SummaryPrinter


class Application:
    def __init__(self):
        self.save_directory = ""
        self.results: List[Tuple[str, str]] = []

    async def run(self) -> None:
        # получение путя
        validator = PathValidator()
        self.save_directory = validator.get_valid_save_directory()
        print(f"Selected directory: {self.save_directory}")

        # создание асинхронной http-сессии:
        # создание асинх контекстного менеджера для http-сессии,
        # с закрытием после завершения блока
        async with aiohttp.ClientSession() as session:
            # запуск асинх цикла ввода URL
            # и загрузки изображений с ожиданием завершения
            await self._input_loop(session)

        # вывод сводки
        await SummaryPrinter.print_summary(self.results)

    # внутренний метод управления вводом URL от пользователя
    async def _input_loop(self, session: aiohttp.ClientSession) -> None:
        # получение основного цикла событий asyncio, управляющего асинх задачами
        # (синхронные операции могут блокать асинхронные)
        loop = asyncio.get_event_loop()
        # список задач
        tasks = []

        while True:
            # выполнение синх функ инпут в пуле потоков по умолчанию
            # чтобы не блокировать event loop
            url = await loop.run_in_executor(
                None, input, "Enter image URL (empty to finish): ")
            url = url.strip()

            if not url:
                break

            downloader = ImageDownloader(session, self.save_directory)
            # создание асинхронной задачи
            task = asyncio.create_task(downloader.download(url))
            tasks.append(task)

        if tasks:
            print("Waiting for remaining downloads to complete...")
            # ожидание всех задач
            completed = await asyncio.gather(*tasks, return_exceptions=True)
            for result in completed:
                if isinstance(result, tuple):
                    self.results.append(result)
