import datetime

import constants, db_users, account_agent, constants


def init(webdriver):
    constants.init()
    account_agent.login(webdriver)


def update(webdriver):
    start = datetime.datetime.now()
    _check_follow_list(webdriver)
    while True:
        account_agent.follow_people(webdriver)
        end = datetime.datetime.now()
        elapsed = end - start

        if elapsed.total_seconds() >= constants.CHECK_FOLLOWERS_EVERY:
            start = datetime.datetime.now()
            _check_follow_list(webdriver)


def _check_follow_list(webdriver):
    print("Checking for users to unfollow")

    users = db_users.check_unfollow_list()

    if len(users) > 0:
        account_agent.unfollow_people(webdriver, users)