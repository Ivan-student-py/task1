from image_link_handler.application import Application
import asyncio


if __name__ == "__main__":
    app = Application()
    asyncio.run(app.run())
