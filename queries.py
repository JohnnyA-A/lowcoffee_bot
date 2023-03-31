import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def getMenu(cursor):
	cursor.execute("""SELECT * FROM "menu"; """)
	record = cursor.fetchall()
	print("Результат", record[0])


def takeOrderId(cursor):
	cursor.execute("""SELECT * FROM "orders";""")
	record = cursor.fetchall()
	if record:
		return int(record[len(record) - 1][0]) + 1
	else:
		return 1

def makeOrder(cursor, order):
	for i in order:
		comm = """INSERT INTO "orders" VALUES ('{}', '{}', {}, {});""".format(i[0], i[1], i[2], i[3])
		cursor.execute(comm)
		connection.commit()

try:
    connection = psycopg2.connect(user="postgres",
                                  password="qwerty",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="coffee_bot")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    order = [[takeOrderId(cursor), "Капучино", 0.3, 1], [takeOrderId(cursor) + 1, "Латте", 0.3, 1] ]
    makeOrder(cursor, order)
except (Exception, Error) as error:
    print("Ошибка на сервере, попробуйте заказать позже", error)
