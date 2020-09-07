import psycopg2

import constants


class DbHandler():

    def __init__(self):

        self.HOST = constants.DB_HOST
        self.USER = constants.DB_USER
        self.PASSWORD = constants.DB_PASS
        self.DBNAME = constants.DB_NAME

    obj = constants.init()

    HOST = constants.DB_HOST
    USER = constants.DB_USER
    PASSWORD = constants.DB_PASS
    DBNAME = constants.DB_NAME

    @staticmethod
    def get_mydb():
        if DbHandler.DBNAME == '':
            constants.init()
        db = DbHandler()
        mydb = db.connect()

        return mydb

    def connect(self):
        conn = psycopg2.connect(
            database=DbHandler.DBNAME,
            user=DbHandler.USER,
            password=DbHandler.PASSWORD,
            host=DbHandler.HOST,
        )
        return conn
