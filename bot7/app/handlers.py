from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from app.db import save_to_db, get_user_schedule, delete_schedule
from datetime import datetime

router = Router()

class Student(StatesGroup):
    waiting_for_time = State()

@router.message(Command("set_schedule"))
async def set_schedule(message: types.Message, state: FSMContext):
    await message.answer("Укажите время в формате HH:MM, например: 12:34.")
    await state.set_state(Student.waiting_for_time)

@router.message(Student.waiting_for_time)
async def set_time(message: types.Message, state: FSMContext):
    time = message.text.strip()
    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        await message.answer("Неправильный формат времени, используйте формат HH:MM.")
        return

    save_to_db(message.from_user.id, time)
    await message.answer(f"Напоминание установлено на {time}")
    
    await state.clear()

@router.message(Command("view_schedule"))
async def view_schedule(message: types.Message):
    schedule = get_user_schedule(message.from_user.id)
    if not schedule:
        await message.answer("У вас нет запланированных заданий.")
        return
    await message.answer("Ваше расписание:\n" + "\n".join(schedule))

@router.message(Command("delete_schedule"))
async def delete_schedule(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите время для удаления задачи, например: /delete_schedule 10:30")
        return
    time = args[1].strip()

    delete_schedule(message.from_user.id, time)
    await message.answer(f"Задача на {time} была удалена.")
