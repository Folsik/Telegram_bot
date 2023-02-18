import logging
import sqlite3 as sq
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

TOKEN = ""
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=TOKEN)
disp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print("Бот вышел в онлайн")
    sqlite_start()

"""Client_bot: Part of the program code for interacting with the client"""


@disp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Привет я помогу тебе записаться мастеру", reply_markup=cb)
        await message.delete()
    except:
        await message.reply("Для общения с ботом напишите ему\nhttps://t.me/Barb_shop_bot")


@disp.message_handler(commands=["Time_work"])
async def barber_time_work(message: types.Message):
    await bot.send_message(message.from_user.id, "Ежедневно с 10:00 до 22:00")


@disp.message_handler(commands=["Address"])
async def barber_address(message: types.Message):
    await bot.send_message(message.from_user.id, "Москва")


@disp.message_handler(commands=["service"])
async def service_barb(message: types.Message):
    for x in cur.execute("SELECT * FROM service").fetchall():
        await bot.send_photo(message.from_user.id, x[0], f"{x[1]}\nОписание: {x[2]}\nЦена: {x[-1]}")

"""Admin_bot: This part of the code is for administration"""


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


def sqlite_start():
    global base, cur
    base = sq.connect("barber.db")
    cur = base.cursor()
    if base:
        print("Data base connected")
    base.execute("CREATE  TABLE IF NOT EXISTS service(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)")
    base.commit()


async def sqlite_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO service VALUES(?, ?, ?, ?)", tuple(data.values()))
        base.commit()


async def sqlite_reed():
    return cur.execute("SELECT * FROM service").fetchall()


async def sqlite_delete_command(data):
    cur.execute("DELETE FROM service WHERE name == ?", (data,))
    base.commit()


@disp.message_handler(commands=["moderator"], is_chat_admin=True)
async def chang_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Режим настройки", reply_markup=button_admin)
    await message.delete()


@disp.message_handler(commands=["Download"], state=None)
async def adm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply("Загрузить фото")


@disp.message_handler(state="*", commands=["cancel"])
@disp.message_handler(Text(equals=["cancel"], ignore_case=True), state="*")
async def cancel(message: types.Message, state: FSMContext):
    status = await state.get_state()
    if status is None:
        return
    await state.finish()
    await message.reply("Ok")


@disp.message_handler(content_types=["photo"], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Название: ")


@disp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply("Описание: ")


@disp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        await message.reply("Цена: ")


@disp.message_handler(state=FSMAdmin.price)
async def load_prise(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["price"] = message.text
        await sqlite_command(state)
    await state.finish()


@disp.callback_query_handler(lambda x: x.data and x.data.startswith("Del"))
async def delete_run(query: types.CallbackQuery):
    await sqlite_delete_command(query.data.replace('Del ', ' '))
    await query.answer(text=f"{query.data.replace('Del ',' ')} удалена", show_alert=True)


@disp.message_handler(commands=["Delete"])
async def delete_service(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_reed()
        for x in read:
            await bot.send_photo(message.from_user.id, x[0], f"{x[1]}\nОписание: {x[2]}\nЦена: {x[-1]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f"Удалить {x[1]}", callback_data=f"Del {x[1]}")))


"""Common_bot: The general part of the program code"""


@disp.message_handler()
async def text(message: types.Message):
    await message.answer(message.text)


button_one = KeyboardButton("/Time_work")
button_two = KeyboardButton("/Address")
button_three = KeyboardButton("/Services")
button_four = KeyboardButton("My number phone", request_contact=True) #Для записи
button_five = KeyboardButton("/Download")
button_six = KeyboardButton("/Delete")


cb = ReplyKeyboardMarkup(resize_keyboard=True)
cb.row(button_one, button_two).add(button_three)
button_admin = ReplyKeyboardMarkup(resize_keyboard=True)
button_admin.row(button_five, button_six)


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True, on_startup=on_startup)
