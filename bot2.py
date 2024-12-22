from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import TOKEN
import asyncio



token = (TOKEN)


bot = Bot(token)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):

    welcome_message = "Привет! Я — информационный бот. Я могу предоставить информацию по следующим темам:"
    
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Новости'))
    keyboard.add(KeyboardButton('Курсы валют'))
    keyboard.add(KeyboardButton('Контактная информация'))
    keyboard.add(KeyboardButton('Часто задаваемые вопросы'))
    

    await message.answer(welcome_message, reply_markup=keyboard)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = """
    Я могу предоставить информацию по следующим темам:
    1. Новости — Узнайте последние новости.
    2. Курсы валют — Текущие курсы валют.
    3. Контактная информация — Наши контактные данные.
    4. FAQ — Часто задаваемые вопросы.

    Используйте /start для начала работы, /menu для отображения главного меню.
    """
    await message.answer(help_text)

@dp.message(Command('about'))
async def about(message: types.Message):
    about_text = "Этот бот предоставляет актуальную информацию по различным темам. Разработан для удобства пользователей."
    await message.answer(about_text)


@dp.message(Command('menu'))
async def menu(message: types.Message):
    await send_welcome(message)

@dp.message(lambda message: message.text in ['Новости', 'Курсы валют', 'Контактная информация', 'Часто задаваемые вопросы'])
async def respond_to_query(message: types.Message):
    text = message.text
    
    if text == 'Новости':
        response = "Сегодня: курс доллара вырос на 2%, акции падают."
    elif text == 'Курсы валют':
        response = "Доллар: 86c, Евро: 90."
    elif text == 'Контактная информация':
        response = "Наша почта: info@exemple.com. Телефон: +123456789."
    elif text == 'Часто задаваемые вопросы':
        response = "Вопрос: До скольких работаем?\nОтвет: Мы работаем до 17:00"
    
    await message.answer(response)


async def on_start():
    await dp.start_polling(bot)

if __name__ == '__main__':
    
    asyncio.run(on_start())