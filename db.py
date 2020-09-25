from contextlib import closing

import pymysql
from pymysql import Error
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

class Dbase(object):

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def insert(self, id):
        conn = 0
        try:
            conn = pymysql.connect(host=self.host,
                                           database=self.database,
                                           user=self.user,
                                           password=self.password)
            query = "INSERT INTO pysha.users value (" + id + ");"
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

        except Error as e:
            print(e)

        finally:
                conn.close()


    def check(self, id):
        conn = 0
        try:
            conn = pymysql.connect(host=self.host,
                                           database=self.database,
                                           user=self.user,
                                           password=self.password)
            query = "select count(*) as count from pysha.users where id="+ str(id) +";"
            cursor = conn.cursor()
            cursor.execute(query)
            for i in cursor:
                if i[0] == 0:
                    return False
                else:
                    return True

        except Error as e:
            print(e)

        finally:
                conn.close()

