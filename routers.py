from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import add_order

order_router = Router()

class OrderState(StatesGroup):
    product = State()
    address = State()
    phone = State()
    confirm = State()


@order_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Что хотите заказать?")
    await state.set_state(OrderState.product)

@order_router.message(OrderState.product)
async def get_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text)
    await message.answer("Укажите адрес доставки:")
    await state.set_state(OrderState.address)

@order_router.message(OrderState.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Укажите ваш номер телефона:")
    await state.set_state(OrderState.phone)

@order_router.message(OrderState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш заказ:\nТовар: {data['product']}\nАдрес: {data['address']}\nТелефон: {data['phone']}\nПодтверждаете?")
    await state.set_state(OrderState.confirm)

@order_router.message(OrderState.confirm, F.text.lower().in_(["да", "нет"]))
async def confirm_order(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        user_id = message.from_user.id
        add_order(user_id, data['product'], data['address'], data['phone'])
        await message.answer("Заказ принят! Спасибо!")
    else:
        await message.answer("Заказ отменен.")
    