from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging
from config import TOKEN

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token = TOKEN)
dp = Dispatcher()

AUTOPARTS = {
    'Лобовое Стекло' : 150,
    "Передний Бампер" : 150,
    "Задний Бампер" : 150,
    "Диски Кованные 4х" : 150 ,
    "Тонировка": 50
}
PHONEPARTS = {
    'Дисплей' : 350,
    "Корпус" : 50,
    "Батарея" : 100,
    "Заднии Камеры" : 200 ,
    "Чистка динамиков": 20
}



GENDER = [
    "Мужской",
    "Женский"
]

orders = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()

    for gender in GENDER:
        builder.button(
            text=gender,
            callback_data=f"info_{gender.lower()}"
        )
    builder.adjust(1)

    await message.answer("Добро пожаловать.\nВыберите из меню: /APmenu, /PPmenu", reply_markup=builder.as_markup())

@dp.message(F.text == "Мужской")
async def about(message:types.Message):
    await message.answer("Выберите что вы бы хотели бы купить Автозапчасти:/APmenu, Запчасти для смартфона:/PPmenu")

@dp.message(Command("APmenu"))
async def menu(message:types.Message):
    builder = InlineKeyboardBuilder()

    for part, price in AUTOPARTS.items():
        builder.button(
            text=f"{part} - {price}",
            callback_data=f"menu_{part}"
        )
    builder.adjust(2)
    await message.answer("Меню АвтоЗапчестей: ", reply_markup=builder.as_markup())

@dp.message(Command("PPmenu"))
async def menu(message:types.Message):
    builder = InlineKeyboardBuilder()

    for phonepart, price in PHONEPARTS.items():
        builder.button(
            text=f"{phonepart} - {price}",
            callback_data=f"menu_{phonepart}"
        )
    builder.adjust(2)
    await message.answer("Меню Запчастей для телефона: ", reply_markup=builder.as_markup())



@dp.callback_query(F.data.startswith('menu_'))
async def choose_autopart(callback: types.CallbackQuery):
    part = callback.data.split("_")[1]
    orders[callback.from_user.id] = {"part" : part}

    builder = InlineKeyboardBuilder()
    for i in range(1,5):
        builder.button(
            text=str(i),
            callback_data=f"quantity_{i}"
        )    
    builder.adjust(3)
    await callback.message.answer(
        f"Вы выбрали {part}. Укажите кол-во:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith('quantity_'))
async def choose_quantity(callback: types.CallbackQuery):
    quantity = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if user_id in orders:
        orders[user_id]["quantity"] = quantity
        part = orders[user_id]["part"]
        price = AUTOPARTS or PHONEPARTS

        builder = InlineKeyboardBuilder()
        builder.button(
                text="Потвердить Заказ",
                callback_data="confirm_orders"
            )    
        
        await callback.message.answer(
            f"Ваш заказ: {part} = {price} денег.\nПодтвердите заказ",
            reply_markup=builder.as_markup()                                     
                                      )


@dp.callback_query(F.data.startswith('menu_'))
async def choose_phonepart(callback: types.CallbackQuery):
    phonepart = callback.data.split("_")[1]
    orders[callback.from_user.id] = {"phonepart" : phonepart}

    builder = InlineKeyboardBuilder()
    for i in range(1, 5):
        builder.button(
            text=str(i),
            callback_data=f"quantity_{i}"
        )    
    builder.adjust(3)
    await callback.message.answer(
        f"Вы выбрали {phonepart}. Укажите кол-во:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith('quantity_'))
async def choose_quantity(callback: types.CallbackQuery):
    quantity = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if user_id in orders:
        orders[user_id]["quantity"] = quantity
        phonepart = orders[user_id]["phonepart"]
        price = PHONEPARTS[phonepart] * quantity 

        builder = InlineKeyboardBuilder()
        builder.button(
                text="Подтвердить заказ",
                callback_data="confirm_orders"
            )    

        await callback.message.answer(
            f"Ваш заказ: {phonepart} x {quantity} = {price} денег.\nПодтвердите заказ",
            reply_markup=builder.as_markup()                                     
        )




async def main():
    await dp.start_polling(bot)

asyncio.run(main())
