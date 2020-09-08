import datetime
from time import sleep

import constants
from db_handler import DbHandler
from bot import InstagramBot


def main():
    username = constants.INST_USER
    password = constants.INST_PASS
    hashtags = constants.HASHTAGS
    likes_over = constants.LIKES_OVER
    check_followers_every = constants.CHECK_FOLLOWERS_EVERY
    days_to_unfollow = constants.DAYS_TO_UNFOLLOW

    start = datetime.datetime.now()

    instagram_bot = InstagramBot(username, password)
    instagram_bot.login()
    instagram_bot.unfollow_new_followed_list()

    instagram_bot.follow_people(hashtags, interactions=3)

    # db = DbHandler()
    # people_to_unfollow = db.get_followed_list()
    # instagram_bot.unfollow_people(people_to_unfollow)

    end = datetime.datetime.now()
    elapsed = end - start

    if elapsed.total_seconds() >= check_followers_every:
        start = datetime.datetime.now()
        instagram_bot.unfollow_new_followed_list()

    # followers = instagram_bot.get_follow_list(which_list='following')
    # breakpoint()
    # for hashtag in hashtags:
    #     instagram_bot.go_to_hashtags_pages(hashtags)
    #     # do stuff

if __name__ == '__main__':
    main()
