from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import sqlite3
import os


from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token = API_TOKEN)

dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message:types.Message):
    await message.answer(
        "Добро пожаловать, этот бот может отправить письмо по электронной почте кому угодно. Нажмите /sendmail чтобы продолжить."       
    )

@dp.message(Command("sendmail"))
async def get_text(message:types.Message):
    await message.answer(
        
    )    