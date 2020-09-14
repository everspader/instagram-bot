import datetime

import psycopg2

from bot import constants
from bot import time_helper


class DbHandler():
    """
    Class to handle the connection to the Postgres database
    and define methods for retrieving information from followers
    database.
    """

    def __init__(self):
        self.HOST = constants.DB_HOST
        self.USER = constants.DB_USER
        self.PASSWORD = constants.DB_PASS
        self.DBNAME = constants.DB_NAME

        self.conn = psycopg2.connect(
            database=self.DBNAME,
            user=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
        )

    def delete_user(self, username):
        """Delete a new followed user entry from database"""
        cursor = self.conn.cursor()
        sql = f"DELETE FROM followers WHERE username = '{username}'"
        cursor.execute(sql)
        self.conn.commit()

    def add_user(self, username):
        """Add a new followed user entry to database"""
        cursor = self.conn.cursor()
        now = datetime.datetime.now().date()
        sql = (f"INSERT INTO followers(username, date_added) "
               f"VALUES('{username}', '{now}')")
        cursor.execute(sql)
        self.conn.commit()

    def get_unfollow_list(self):
        """
        Return a list of users that can be unfollowed based on the DAYS_TO_UNFOLLOW setting
        specified in the settings.json
        """
        cursor = self.conn.cursor()
        sql = "SELECT * FROM followers"
        cursor.execute(sql)
        results = cursor.fetchall()
        users_to_unfollow = []
        for r in results:
            d = time_helper.days_since_date(r[1])
            if d > constants.DAYS_TO_UNFOLLOW:
                users_to_unfollow.append(r[0])

        return users_to_unfollow

    def get_followed_list(self):
        """Return a list of all the new users that the bot followed"""
        users = []
        cursor = self.conn.cursor()
        sql = "SELECT * FROM followers"
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            users.append(r[0])

        return users
