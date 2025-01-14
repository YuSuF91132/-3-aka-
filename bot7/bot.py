import asyncio
from aiogram import Dispatcher, Bot
from app.start import router as start
from app.handlers import router
from app.db import init_db
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.environ.get("token"))
dp = Dispatcher()

async def main():
    print("Запуск бота")

    init_db()

    dp.include_router(start)
    dp.include_router(router)
    await dp.start_polling(bot)
try:
    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    print("Выход")