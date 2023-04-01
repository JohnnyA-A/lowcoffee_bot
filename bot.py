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
        btn = [types.KeyboardButton("Капучино 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Капучино 0.4 - {}p.".format(record[tmp][2])), types.KeyboardButton("Капучино 0.5 - {}p.".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Латте - 120р./150р./170р."):
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        #await message.delete()
        tmp = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = [types.KeyboardButton("Латте 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Латте 0.4 - {}p.".format(record[tmp][2])), types.KeyboardButton("Латте 0.5 - {}p.".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Мокко - 145р./175р./195р."):
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        #await message.delete()
        tmp = 2
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = [types.KeyboardButton("Мокко 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Мокко 0.4 - {}p.".format(record[tmp][2])), types.KeyboardButton("Мокко 0.5 - {}p.".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Флэт Уайт - 140р./170р./190р."):
        cursor.execute("""SELECT * FROM "menu"; """)
        record = cursor.fetchall()
        #await message.delete()
        tmp = 3
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = [types.KeyboardButton("Флэт Уайт 0.3 - {}р.".format(record[tmp][1])), types.KeyboardButton("Флэт Уайт 0.4 - {}p.".format(record[tmp][2])), types.KeyboardButton("Флэт Уайт 0.5 - {}p.".format(record[tmp][3]))]
        for i in btn:
            markup.add(i)
        await bot.send_message(message.chat.id, text="Выберите размер", reply_markup=markup)
    elif (message.text == "Капучино 0.3 - 120р.") or (message.text == "Капучино 0.4 - 150p.") or (message.text == "Капучино 0.5 - 170p.") or (message.text == "Латте 0.3 - 120р.") or (message.text == "Латте 0.4 - 150p.") or (message.text == "Латте 0.5 - 170p.") or (message.text == "Мокко 0.3 - 145р.") or (message.text == "Мокко 0.4 - 175p.") or (message.text == "Мокко 0.5 - 195p.") or (message.text == "Флэт Уайт 0.3 - 140р.") or (message.text == "Флэт Уайт 0.4 - 170p.") or (message.text == "Флэт Уайт 0.5 - 190p.") :
        price = message.text[::-1]
        price = price[2:5]
        price = int(price[::-1])
        PRICE = types.LabeledPrice(label=message.text.split()[0] , amount=price*100)  # в копейках (руб)
        cursor.execute("""SELECT * FROM "orders";""")
        record = cursor.fetchall()
        if record:
            orderId = int(record[len(record) - 1][0]) + 1
        else:
            orderId = 1
        comm = """INSERT INTO "orders" VALUES ('{}', '{}', {}, {});""".format(orderId, message.text.split()[0] , message.text.split()[1], price)
        cursor.execute(comm)
        connection.commit()


        await bot.send_invoice(message.chat.id,
                           title="Ваш заказ",
                           description=message.text,
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    else:
        await bot.send_message(message.chat.id, text="Такой команды ещё нет")
# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")


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
        