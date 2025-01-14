import os
import asyncio
import logging
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import email_validator

load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    email = State()
    message = State()

async def send_email(to_email, message_body):
    message = EmailMessage()
    message.set_content(message_body)
    message['Subject'] = 'Сообщение от бота'
    message['From'] = SMTP_USER
    message['To'] = to_email

    try:
        logging.info(f"Отправка сообщения на {to_email}")
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD
        )
        logging.info("Сообщение успешно отправлено")
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")
        return False

@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.set_state(Form.email)
    await message.answer("Привет! Я бот для отправки эл.писем. Введите адрес электронной почты для отправки.")

@dp.message(Form.email)
async def email_handler(message: types.Message, state: FSMContext):
    user_email = message.text.strip()
    try:
        v = email_validator.validate_email(user_email)
        user_email = v["email"]
        await state.update_data(email=user_email)
        await state.set_state(Form.message)
        await message.answer("Введите текст сообщения.")
    except email_validator.EmailNotValidError as e:
        await message.answer(f"Некорректный email: {e}")

@dp.message(Form.message)
async def message_handler(message: types.Message, state: FSMContext):
    user_message = message.text.strip()
    if not user_message:
        await message.answer("Сообщение не может быть пустым. Введите текст.")
        return

    await state.update_data(message=user_message)
    data = await state.get_data()
    email = data.get("email")
    message_text = data.get("message")

    await message.answer(
        f"Вы хотите отправить следующее сообщение на {email}:\n\n"
        f"{message_text}\n\nПодтвердите отправку (Да/Нет)."
    )

@dp.message(lambda message: message.text.lower() in ["да", "нет"])
async def confirmation_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        email = data.get("email")
        message_text = data.get("message")
        if await send_email(email, message_text):
            await message.answer("Сообщение успешно отправлено!")
        else:
            await message.answer("Не удалось отправить сообщение. Проверьте настройки SMTP.")
    else:
        await message.answer("Отправка отменена.")

    await state.finish()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())