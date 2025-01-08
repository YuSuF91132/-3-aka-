import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

import routers
from database import create_tables

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token = API_TOKEN)
    dp = Dispatcher()

    create_tables()

    dp.include_router(routers.order_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())