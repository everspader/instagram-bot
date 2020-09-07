import datetime

import constants
import time_helper
from db_handler import DbHandler


def delete_user(username):
    """Delete a new followed user entry from database"""
    conn = DbHandler.get_mydb()
    cursor = conn.cursor()
    sql = f"DELETE FROM followers WHERE username = '{username}'"
    cursor.execute(sql)
    conn.commit()


def add_user(username):
    """Add a new followed user entry to database"""
    conn = DbHandler.get_mydb()
    cursor = conn.cursor()
    now = datetime.datetime.now().date()
    sql = f"INSERT INTO followers(username, date_added) VALUES('{username}', '{now}')"
    cursor.execute(sql)
    conn.commit()


def check_unfollow_list():
    """
    Return a list of users that can be unfollowed based on the DAYS_TO_UNFOLLOW setting
    specified in the settings.json
    """
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
    """Return a list of all the new users that the bot followed"""
    users = []
    conn = DbHandler.get_mydb()
    cursor = conn.cursor()
    sql = "SELECT * FROM followers"
    cursor.execute(sql)
    results = cursor.fetchall()
    for r in results:
        users.append(r[0])

    return users