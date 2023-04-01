import config
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,\
 KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# установка уровня логирования
logging.basicConfig(level=logging.INFO)

# инициализация бота и диспетчера
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
admins = [450284324] 
#895230164
# реализация команды '/start'
@dp.message_handler(commands=['start'])
async def start(message):
    if message.from_user.id in admins:
        await message.delete()
        await bot.send_message(message.chat.id, text="Привет admin", reply_markup=markup)
    else:
        await user_func(message)
async def user_func(message):
    await message.delete()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await bot.send_message(message.chat.id, text="Привет! У нас ты можешь дистанционно заказать кофе!", reply_markup=markup)
    btn1 = types.KeyboardButton("Гороховая 35-37")
    btn2 = types.KeyboardButton("Садовая 38")
    btn3 = types.KeyboardButton("Садовая 44")
    btn4 = types.KeyboardButton("Попова 30")
    btn5 = types.KeyboardButton("Ломоносова 20")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    await bot.send_message(message.chat.id, text="Выбери кофейню", reply_markup=markup)
@dp.message_handler(content_types=['text'])
def cafe(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "Гороховая 35-37":
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        btn = []
        for i in record:
            btn.append(types.KeyboardButton(i[0]))
        for i in btn:
            markup.add(i)


# запуск бота
global cursor, connection
        
if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="qwerty",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="lowcoffee_bot")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        executor.start_polling(dp, skip_updates=False)
    except (Exception, Error) as error:
        print("Ошибка на сервере, попробуйте заказать позже", error)
        