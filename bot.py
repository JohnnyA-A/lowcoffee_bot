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
admins = [] 
#450284324
#895230164


# реализация команды '/start'
@dp.message_handler(commands=['start'])
async def start(message):
    if message.from_user.id in admins:
        #await message.delete()
        #тут нет markup
        await bot.send_message(message.chat.id, text="Привет admin", reply_markup=markup)
    else:
        await user_func(message)



async def user_func(message):
    #await message.delete()
    btn = [[KeyboardButton("Гороховая 35-37")], [KeyboardButton("Садовая 38")], [KeyboardButton("Садовая 44")], [KeyboardButton("Попова 30")], [KeyboardButton("Ломоносова 20")] ]
    await bot.send_message(message.chat.id, text="Привет! У нас ты можешь дистанционно заказать кофе!")
    await bot.send_message(message.chat.id, text="Выберите кофейню", reply_markup=ReplyKeyboardMarkup(btn))


@dp.message_handler(content_types=['text'])
async def cafe(message):
    #await message.delete()
    cursor.execute("""SELECT * FROM "menu"; """)
    record = cursor.fetchall()
    btn = []
    for i in record:
        btn.append([KeyboardButton("{}  - {}р./{}р./{}р.".format(i[0], i[1], i[2], i[3]))])
    await bot.send_message(message.chat.id, text="Выберите кофе", reply_markup=ReplyKeyboardMarkup(btn))

@dp.message_handler(content_types=['text'])
async def coffee(message):
    #await message.delete()
    print('1')
    cursor.execute("""SELECT 'smallPrice' FROM "menu" WHERE 'coffeeName'='Капучино';""")
    record = cursor.fetchall()
    print(record)
    btn = [[KeyboardButton("0.3 - {}р.".format(1))], [KeyboardButton("0.4 - {}.p".format(1))], [KeyboardButton("0.5 - {}.p".format(1))]]
    for i in record:
        btn.append([KeyboardButton(i[0])])
    await bot.send_message(message.chat.id, text="Выберите кофе".format(message.text), reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True))
    

# запуск бота
global cursor, connection, msgs

if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="qwerty",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="lowcoffee_bot")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        msgs = []
        executor.start_polling(dp, skip_updates=False)
    except (Exception, Error) as error:
        print("Ошибка на сервере, попробуйте заказать позже", error)
        