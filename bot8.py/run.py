from aiogram import Bot, Dispatcher
import asyncio, logging, os
# from dotenv import load_dotenv
from router import router 

logging.basicConfig(level=logging.DEBUG)

# load_dotenv()

# bot = Bot(token=os.getenv("token"))
bot = Bot("8158021530:AAFz8Ycb_QP6ikvD8-dJLSS-BB1gRiPdEeU") 
dp = Dispatcher()

async def main():
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())