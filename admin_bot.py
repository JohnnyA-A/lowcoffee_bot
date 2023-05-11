import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


if __name__ == "__main__":
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="qwerty",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="lowcoffee_bot")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        cursor.execute("""UPDATE "orders" SET "order_status"=0 WHERE "orderId"=19;""")
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка на сервере, попробуйте заказать позже", error)