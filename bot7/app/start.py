from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Здравствуйте! Я бот для планирования задач. Вот что я могу:\n"
        "/set_schedule <время> - Установить задачу\n"
        "/view_schedule - Посмотреть график задач\n"
        "/delete_schedule <время> - Удалить задачу\n"
        "/update_schedule <старое время> <новое время> - Обновить задачу"
    )
