import os  # для работы с путями
import asyncio  # основа асинхронности
import aiohttp  # для асинхронных http-запросов (нужно установить)


class ImageDownloader:
    def __init__(self):
        # всегда строковое поле у объекта класса
        self.save_directory: str = ""
        # список кортежей ссылок и статусов
        self.results: list[tuple[str, str]] = []
        # для контроля сессии (возможно придётся заменить)
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
        print(f"Selected directory: {self.save_directory}")

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

    # внутренний метод управления вводом URL от пользователя
    async def _input_loop(self) -> None:
        # получение основного цикла событий asyncio, управляющего асинх задачами
        # (синхронные операции могут блокать асинхронные)
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

            # создание асинхронной задачи
            task = asyncio.create_task(self._download_image(url))
            tasks.append(task)

        if tasks:
            print("Waiting for remaining downloads to complete...")
            # ожидание всех задач
            await asyncio.gather(*tasks, return_exceptions=True)

    # метод скачивания содержимого по HTTP
    async def _download_image(self, url: str) -> None:
        try:
            # ГЕТ-запрос
            async with self.session.get(url) as response:
                # по умолчанию aiohttp не выбрасывает исключение
                # при 404/500
                if response.status != 200:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"HTTP {response.status}"
                    )
                content = await response.read()

            # извлечение имени файла из URL,
            # если URL заканчивается на / , то filename="" ->
            # подставляется заглушка
            filename = url.split('/')[-1]
            if not filename:
                filename = "image_without_name"
            filepath = os.path.join(self.save_directory, filename)

            # сохранение через run_in_executor
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._save_file,
                                       filepath, content)

            self.results.append((url, "Success"))

        except Exception:
            self.results.append((url, "Error"))

    # отдельный метод сохранения
    def _save_file(self, filepath: str, content: bytes) -> None:
        with open(filepath, 'wb') as f:
            f.write(content)

    # async метод, для сохранения единообразия с другими методами
    async def _print_summary(self) -> None:
        print("\nSummary of succesful and unsuccessful downloads")

        max_url_len = max(len(url)
                          for url, _ in self.results) if self.results else 0
        col_width_url = min(max(66, max_url_len), 80)
        col_width_status = 10

        border = "+" + "-" * (col_width_url + 2) + "+" + \
            "-" * (col_width_status + 2) + "+"
        header_url = "Link".ljust(col_width_url)
        header_status = "Status".ljust(col_width_status)

        print(border)
        print(f"| {header_url} | {header_status} |")
        print(border)

        for url, status in self.results:
            url_display = url.ljust(col_width_url)
            status_display = status.ljust(col_width_status)
            print(f"| {url_display} | {status_display} |")

        print(border)


if __name__ == "__main__":
    downloader = ImageDownloader()
    asyncio.run(downloader.run())
