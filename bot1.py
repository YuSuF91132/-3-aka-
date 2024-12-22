from aiogram import Bot, Dispatcher, types, 
from aiogram.filters import Command
import asyncio
import random
from config import token

bot=Bot(token=token)
dp=Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши 'Камень', 'Ножницы' или 'Бумага', чтобы начать игру.")

@dp.message()
async def randomm(message:types.Message):
    bot_choice=random.choice(['Камень', 'Ножницы', 'Бумага'])
    user_choice=message.text
    if user_choice==bot_choice:
        await message.answer(f'Ничья. Бот выбрал: {bot_choice}')
    elif user_choice=='Камень' and bot_choice=='Ножницы':
        await message.answer(f'Победа. Бот выбрал: {bot_choice}')
    elif user_choice=='Ножницы' and bot_choice=='Бумага':
        await message.answer(f'Победа. Бот выбрал: {bot_choice}')
    elif user_choice=='Бумага' and bot_choice=='Камень':
        await message.answer(f'Победа. Бот выбрал: {bot_choice}')
    else:
        await message.answer(f'Поражение.  Бот выбрал: {bot_choice}')

async def main():
        await dp.start_polling(bot)
if __name__ == '__main__':
    try:
         asyncio.run(main())
    except KeyboardInterrupt:
        print('Ошибка:KeyboardInterrupt')