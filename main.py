import datetime
import sys
from time import sleep

from bot import constants, InstagramBot


def main():
    username = constants.INST_USER
    password = constants.INST_PASS
    hashtags = constants.HASHTAGS
    likes_over = constants.LIKES_OVER
    check_followers_every = constants.CHECK_FOLLOWERS_EVERY
    days_to_unfollow = constants.DAYS_TO_UNFOLLOW

    start = datetime.datetime.now()

    instagram_bot = InstagramBot()
    instagram_bot.login(username, password)

    instagram_bot.unfollow_new_followed_list()
    instagram_bot.follow_people_from_hashtags(hashtags, interactions=3)

    end = datetime.datetime.now()
    elapsed = end - start

    if elapsed.total_seconds() >= check_followers_every:
        start = datetime.datetime.now()
        instagram_bot.unfollow_new_followed_list()

    instagram_bot.end_session()

if __name__ == '__main__':
    main()

    data = None
    if len(sys.argv) != 2:
        print("Usage: main.py settings-prod.json")
    else:
        settings_bot = sys.argv[1]

    constants.constants(settings_bot)
    main()