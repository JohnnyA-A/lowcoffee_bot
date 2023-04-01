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
    btn = [types.KeyboardButton("Гороховая 35-37"), types.KeyboardButton("Садовая 38"), types.KeyboardButton("Садовая 44"), types.KeyboardButton("Попова 30"), types.KeyboardButton("Ломоносова 20") ]
    await bot.send_message(message.chat.id, text="Привет! У нас ты можешь дистанционно заказать кофе!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in btn:
        markup.add(i)
    await bot.send_message(message.chat.id, text="Выберите кофейню", reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def main(message):
    if (message.text == "Гороховая 35-37") or (message.text == "Садовая 38") or (message.text == "Садовая 44") or (message.text == "Попова 30") or (message.text == "Ломоносова 20"): 
        #await message.delete()
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        btn = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in record:
            btn.append(types.KeyboardButton("{} - {}р./{}р./{}р.".format(i[0], i[1], i[2], i[3])))
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите кофе", reply_markup=markup)
    elif (message.text == "Капучино - 120р./150р./170р."):
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        #await message.delete()
        tmp = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = [types.KeyboardButton("Капучино 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Капучино 0.4 - {}.p".format(record[tmp][2])), types.KeyboardButton("Капучино 0.5 - {}.p".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Латте - 120р./150р./170р."):
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        #await message.delete()
        tmp = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = [types.KeyboardButton("Латте 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Латте 0.4 - {}.p".format(record[tmp][2])), types.KeyboardButton("Латте 0.5 - {}.p".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Мокко - 145р./175р./195р."):
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        #await message.delete()
        tmp = 2
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = [types.KeyboardButton("Латте 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Латте 0.4 - {}.p".format(record[tmp][2])), types.KeyboardButton("Латте 0.5 - {}.p".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Флэт Уайт - 140р./170р./190р."):
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        #await message.delete()
        tmp = 3
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = [types.KeyboardButton("Флэт Уайт 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Флэт Уайт 0.4 - {}.p".format(record[tmp][2])), types.KeyboardButton("Флэт Уайт 0.5 - {}.p".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Капучино 0.3 - 120р."):
        
    else:
        await bot.send_message(message.chat.id, text="Такой команды ещё нет")
    

# запуск бота
global cursor, connection, order
order = []

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
        