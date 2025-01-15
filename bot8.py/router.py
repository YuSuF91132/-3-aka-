from aiogram import Router, types
from parse import parse_news
from aiogram.filters import Command
import logging

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("""
        Здравствуйте! Я бот для парсинга новостей с сайта\n 
        Для получения новостей /parse\n
        Чтобы получить помощь:/help
        """)
    
@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("""
        Для получения новостей с сайта :/parse\n 
        Бот отобразит последнюю новость с сайта\n
        Пример команды: /parse
        """)

@router.message(Command("parse"))
async def parse(message: types.Message):
    try:
        news = parse_news()
        if news:
            await message.answer("\n".join(news))
        else:
            await message.answer("Не удалось получить новость")
    except Exception as e:
        logging.error(f"Ошибка при парсинге: {e}")
        await message.answer("Error:Произошла ошибка при парсинге новости.")
