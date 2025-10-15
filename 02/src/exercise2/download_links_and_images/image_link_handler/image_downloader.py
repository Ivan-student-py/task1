import os
import asyncio  # основа асинхронности
import aiohttp  # для асинхронных http-запросов (нужно установить)


class ImageDownloader:
    # aiohttp.ClientSession для контроля сессии
    def __init__(self, session: aiohttp.ClientSession, save_directory: str):
        self.session = session
        self.save_directory = save_directory

    async def download(self, url: str) -> tuple[str, str]:
        # Возвращает (url, status)
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
            filename = url.split('/')[-1] or "image_without_name"
            filepath = os.path.join(self.save_directory, filename)

            # сохранение через run_in_executor
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._save_file,
                                       filepath, content)
            return (url, "Success")

        except Exception:
            return (url, "Error")

    # отдельный метод сохранения
    def _save_file(self, filepath: str, content: bytes) -> None:
        with open(filepath, 'wb') as f:
            f.write(content)
