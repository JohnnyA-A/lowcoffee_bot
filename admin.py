import config
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def set_admin(tgId):
	cursor.execute(""" INSERT INTO "admins" VALUES ({}) """.format(tgID))
    connection.commit()
def del_admin(tgId):
	cursor.execute("""DELETE FROM "admins" WHERE admins.admin_id={} """.format(tgID))
    connection.commit()


if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="qwerty",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="lowcoffee_bot")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
    except (Exception, Error) as error:
        print("Ошибка на сервере, попробуйте заказать позже", error)
