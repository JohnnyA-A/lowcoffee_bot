import config
import logging
from aiogram import *
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import CallbackQuery
from time import time, ctime

#for logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

#-------------------------------------------------Classes----------------------------------
class Cafe(object):
    def __init__(self, cafe_id, address, host, port):
        self.id = cafe_id
        self.address = address
        self.host = host
        self.port = port


class Coffee(object):
    def __init__(self, coffeeName, smallVolume, smallPrice, mediumVolume, mediumPrice, bigVolume, bigPrice):
        self.name = coffeeName
        self.smallVolume = smallVolume
        self.smallPrice = smallPrice
        self.mediumVolume = mediumVolume
        self.mediumPrice = mediumPrice
        self.bigVolume = bigVolume
        self.bigPrice = bigPrice

class Order(object):
    def __init__(self, menu_count):
        self.pos_count = 0
        self.names = []
        self.volumes = []
        self.counts = [0] * menu_count * 3
        self.prices = [0] * menu_count * 3
    def add_position(self, coffeeName, coffeeVolume, coffeePrice):
        self.pos_count += 1
        self.names.append(coffeeName)
        self.volumes.append(coffeeVolume)

        for i in range(len(self.names)):
            for k in range(len(self.volumes)):
                if (self.names[i] == coffeeName):
                    if (self.volumes[k] == coffeeVolume):
                        if i == k:
                            self.counts[i] += 1
                            self.prices[i] += coffeePrice
                            return


#------------------------------------------------------------------------------------------



#-----------------------------------------------Functions----------------------------------

#для очистки сообщений
async def messages_del(message):
    i = 0
    while 1:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - i)
            i+=1
        except:
            break


#для удаления глобальных переменных
def globs_del():
    try:
        del order
        del cafes_arr
        del curr_cafe
        del connection
        del cursor
    except:
        pass

#главное меню, меню выбора заведения
async def main_menu(message):
    await messages_del(message)
    #подключение к локальной бд
    try:
        loc_connection = psycopg2.connect(user="postgres",
                                      password="qwerty",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="lowcoffee_cafes")
        loc_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        loc_cursor = loc_connection.cursor()
    except (Exception, Error) as error:
        print("Ошибка на сервере, попробуйте заказать позже", error)
        bot.send_message("Ошибка на сервере, попробуйте заказать позже")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Выбрать заведение"))
        await bot.send_message(message.chat.id, text = "Ошибка на сервере, попробуйте заказать позже", reply_markup=markup)

    loc_cursor.execute("""SELECT * FROM "cafes";""")
    record = loc_cursor.fetchall()
    global cafes_arr
    cafes_arr = []
    for i in record:
        cafes_arr.append(Cafe(i[0], i[1], i[2], i[3]))
    loc_connection.close ()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(i.address) for i in cafes_arr]
    for i in buttons:
        markup.add(i)
    await bot.send_message(message.chat.id, text="Выберите заведение:", reply_markup=markup)


#выбор заведения, меню выбора кофе
async def choose_cafe(message):
    for i in cafes_arr:
        if message.text == i.address:
            global curr_cafe
            curr_cafe = i
    global connection, cursor
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="qwerty",
                                      host=curr_cafe.host,
                                      port=curr_cafe.port,
                                      database="lowcoffee_menu")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
    except (Exception, Error) as error:
        print("Ошибка на сервере, попробуйте заказать позже", error)
        await bot.send_message(message.chat.id, text = "Ошибка на сервере, попробуйте заказать позже")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Выбрать заведение"))
        await bot.send_message(message.chat.id, text = "Ошибка на сервере, попробуйте заказать позже", reply_markup=markup)





    cursor.execute("""SELECT * FROM "menu";""")
    record = cursor.fetchall()
    global menu
    menu = []
    for i in record:
        menu.append(Coffee(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    #объявляем корзину
    global order
    order = Order(len(menu))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Выбрать заведение"))
    await bot.send_message(message.chat.id, text=f"Вы выбрали кофейню по адресу: {curr_cafe.address}", reply_markup=markup)
    
    #показываем кофе из меню
    buttons = [[types.InlineKeyboardButton(text=i.name, callback_data=i.name), types.InlineKeyboardButton(text=f"{i.smallVolume}/{i.smallPrice}р.", callback_data=i.name+"_small"), types.InlineKeyboardButton(text=f"{i.mediumVolume}/{i.mediumPrice}р.", callback_data=i.name+"_medium"), types.InlineKeyboardButton(text=f"{i.bigVolume}/{i.bigPrice}р.", callback_data=i.name+"_big")] for i in menu]
    buttons.append([types.InlineKeyboardButton(text="🛒Корзина", callback_data="cart")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(message.chat.id, text="Выберите кофе:", reply_markup=markup)




async def show_cart(call):
    await messages_del(call.message)
    cart_text = f"Адресс: {curr_cafe.address}\nКофе:|Объем|Количество|Цена\n"
    common_summ = 0
    for i in range(order.pos_count):
        cart_text += f"{order.names[i]}|{order.volumes[i]}|{order.counts[i]}|{order.prices[i]}\n"
        common_summ += order.prices[i]
    await bot.send_message(call.message.chat.id, text=cart_text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Оплатить заказ"), types.KeyboardButton("Назад"))
    await bot.send_message(call.message.chat.id, text=f"Итого:   {common_summ}р.", reply_markup=markup)


async def to_pay(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Выбрать заведение"))
    await bot.send_message(message.chat.id, text=f"При выходе корзина будет опустошена!", reply_markup=markup)
 
    PRICE = types.LabeledPrice(label=message.text.split()[0] , amount=int(sum(order.prices)*100))
    await bot.send_invoice(message.chat.id,
                           title="Ваш заказ",
                           description=message.text,
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

#------------------------------------------------------------------------------------------




#----------------------------------------Bot body------------------------------------------

@dp.message_handler(commands=["start", "help"])
async def welcome_def(message: types.Message):
    await messages_del(message)
    globs_del()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Выбрать заведение")
    await bot.send_message(message.chat.id , text="Добро пожаловать!")
    await bot.send_message(message.chat.id, text="Сеть кофеен\nLowcoffee", reply_markup=markup)

@dp.message_handler(content_types=['text'])
async def main_func(message):
    try:
        # Главное меню и выбор заведения
        if (message.text == "Выбрать заведение"):
            globs_del()
            await messages_del(message)
            await main_menu(message)

        # Выбор заведения и его меню
        elif (message.text in [i.address for i in cafes_arr]) or (message.text == "Назад"):
            await messages_del(message)
            await choose_cafe(message)

        elif (message.text == "Оплатить заказ"):
            await messages_del(message)
            await to_pay(message)
        #Обработка всех непрописанных команд
        else:
            await messages_del(message)
            globs_del()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Выбрать заведение"))
            await bot.send_message(message.chat.id, text = "Такой команды нет :(", reply_markup=markup)
    except NameError:
        await bot.send_message(message.chat.id, text = "Что-то пошло не так, давайте попробуем ещё раз")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Выбрать заведение"))
        await bot.send_message(message.chat.id, text = "Такой команды нет :(", reply_markup=markup)

# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    local_time = ctime(time())
    data = ""
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        data += (f"{k} = {v}")
    cursor.execute("""INSERT INTO "payments" VALUES ('{}', '{}') """.format(local_time, data))
    connection.commit()

    #ищем номер заказа
    cursor.execute("""SELECT * FROM "orders";""")
    record = cursor.fetchall()
    if record:
        orderId = int(record[len(record) - 1][0]) + 1
    else:
        orderId = 1

    await messages_del(message)

    order_names = ""
    order_volumes = ""
    order_counts = ""
    order_prices = ""

    for i in range(order.pos_count):
        order_names += '"' + order.names[i] + '"' +  " ,"
        order_volumes += str(order.volumes[i]) + ","
        order_counts += str(order.counts[i]) + ","
        order_prices += str(order.prices[i]) + ","

    order_names = order_names[:-1]
    order_volumes = order_volumes[:-1]
    order_counts = order_counts[:-1]
    order_prices = order_prices[:-1]
    order_str = f"""INSERT INTO "orders" VALUES ({orderId},""" + "'{" f"{order_names}" "}', '{" f"{order_volumes}" "}', '{" f"{order_counts}" "}', '{" f"{order_prices}" "}')"

    cursor.execute(order_str)
    connection.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Выбрать заведение")

    globs_del()
    await bot.send_message(message.chat.id, text="Ваш номер заказа - {}".format(orderId))   
    await bot.send_message(message.chat.id, text="Не забудьте его", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'cart') 
async def cart(call: CallbackQuery):
    if order.pos_count == 0:
        await call.answer(text="Корзина пока пустая", show_alert=True)
    else:
        await show_cart(call)

@dp.callback_query_handler(lambda c: c.data in [i.name for i in menu]) 
async def coffee_name_press(call: CallbackQuery):
    pass
@dp.callback_query_handler(lambda c: c.data in [i.name+k for k in ["_small", "_medium", "_big"] for i in menu]) 
async def coffee_name_press(call: CallbackQuery):
    tmp = call.data.find("_")
    
    for i in range(len(menu)):
        if menu[i].name == call.data[:tmp]:
            tmp_pos = i
            break
    if call.data[tmp+1:] == "small":
        tmp_vol = 0.3
        tmp_price =  menu[i].smallPrice
    elif call.data[tmp+1:] == "medium":
        tmp_vol = 0.4
        tmp_price =  menu[i].mediumPrice
    elif call.data[tmp+1:] == "big":
        tmp_vol = 0.5
        tmp_price =  menu[i].bigPrice
    order.add_position(call.data[:tmp], tmp_vol, tmp_price)

#------------------------------------------------------------------------------------------



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
