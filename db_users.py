import datetime

from db_handler import DbHandler
import constants
import time_helper



def delete_user(username):
    conn = DbHandler.get_mydb()
    cursor = conn.cursor()
    sql = f"DELETE FROM followers WHERE username = '{username}'"
    cursor.execute(sql)
    conn.commit()


def add_user(username):
    conn = DbHandler.get_mydb()
    cursor = conn.cursor()
    now = datetime.datetime.now().date()
    sql = f"INSERT INTO followers(username, date_added) VALUES('{username}', '{now}')"
    cursor.execute(sql)
    conn.commit()


def check_unfollow_list():
    conn = DbHandler.get_mydb()
    cursor = conn.cursor()
    sql = "SELECT * FROM followers"
    cursor.execute(sql)
    results = cursor.fetchall()
    users_to_unfollow = []
    for r in results:
        d = time_helper.days_since_date(r[1])
        if d > constants.DAYS_TO_UNFOLLOW:
            users_to_unfollow.append(r[0])

    return users_to_unfollow


def get_followed_users():
    users = []
    conn = DbHandler.get_mydb()
    cursor = conn.cursor()
    sql = "SELECT * FROM followers"
    cursor.execute(sql)
    results = cursor.fetchall()
    for r in results:
        users.append(r[0])

    return users