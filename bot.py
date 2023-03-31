import config 
import logging
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)                             
order1 =''
order2 =''
order3 = ''
bot = Bot(token=config.TOKEN)
dp= Dispatcher(bot)
@bot.message_handler(commands=['start'])
def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Гороховая 35-37')
        btn2 = types.KeyboardButton("Садовая 38")
        btn3 = types.KeyboardButton("Садовая 44")
        btn4 = types.KeyboardButton("Попова 30")
        btn5 = types.KeyboardButton("Ломоносова 20")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="выберите кафе для заказа", reply_markup=markup)
 def func(message):
        bot.register_next_step_handler(message, order1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Капучино")
        btn2 = types.KeyboardButton("Американо")
        btn3 = types.KeyboardButton("Латте")
        btn4 = types.KeyboardButton("Мокко")
        btn5 = types.KeyboardButton("Флэт уайт")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="выберите напиток для заказа", reply_markup=markup)
 def func(message):
         bot.register_next_step_handler(message, order2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("0.3")
        btn2 = types.KeyboardButton("0.4")
        btn3 = types.KeyboardButton("0.5")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="выберите объем напитка",  reply_markup=markup)
 bot.register_next_step_handler(message, order3)
 #prices
 PRICE = types.LabeledPrice(label="Ваш заказ:" + order2 + " " + order3  , amount= 500*100) #"запрос в бд тут" * 100)  # в копейках (руб)
 # buy
@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):

    await bot.send_invoice(message.chat.id,
                           title="Ваш заказ",
                           description=order2 + " " + order3,
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           payload="test-invoice-payload")
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
                           f"Платеж на сумму прошел успешно!!!")


# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
    #добавить кнопку поддержка