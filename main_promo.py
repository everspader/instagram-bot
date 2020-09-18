import datetime
import json
import os
import random
import sys
import time
from time import sleep

from bot import constants, InstagramBot, DbHandler


def main(promo_settings):
    """
    Main function to run a promoshare on a specific post according
    to predefined settings.
    """
    end_promo = promo_settings['end_promo']
    end_promo = datetime.datetime.strptime(end_promo, "%d-%m-%Y %H:%M:%S")
    t_start = datetime.datetime.now()

    # BOT INITIALIZATION
    username = constants.INST_USER
    password = constants.INST_PASS
    instagram_bot = InstagramBot()
    instagram_bot.login(username, password)
    db = DbHandler()

    if t_start >= end_promo:
        print("-" * 50 + "\nInstagram promoshare has ended!\n"+ "-" * 50)
        print("Unfollowing remaining users...")
        to_unfollow = db.get_followed_list("to_unfollow")
        instagram_bot.unfollow_people(to_unfollow)
        return

    user = promo_settings['user']
    if not user:
        user = constants.INST_USER

    # If no users are registered in db, then retrieve a specific list of users
    # from the specified user's profile and add them to db.
    user_list_in_db = db.get_followed_list('followers')
    if not user_list_in_db:
        user_list = instagram_bot.get_follow_list(
            user, which_list='followers')
        for u in user_list:
            db.add_user(u, 'followers')
        user_list_in_db = db.get_followed_list('followers')

    post_url = promo_settings['post_url']
    like_post = promo_settings['like_post']
    combine_users = promo_settings['combine_users']
    follow_user = promo_settings['follow_user']
    follow_users_user = promo_settings['follow_users_user']
    mentions = promo_settings['mentions']

    # From the users in the database, get a small random sample to
    # avoid Instagram blocking
    if len(user_list_in_db) > mentions:
        user_list = random.sample(user_list_in_db, mentions)
    else:
        user_list = user_list_in_db

    # BEGIN OF BOT ACTIONS:
    try:
        instagram_bot.go_to_post(post_url)
    except:
        print("You must provide the URL to the post.")
        return

    if like_post:
        instagram_bot.like_post()

    users_to_unfollow = db.get_followed_list('to_unfollow')
    post_user = instagram_bot.get_username_from_post()
    if follow_user and (post_user not in users_to_unfollow):
        instagram_bot.follow_user_on_post()
        db.add_user(post_user, 'to_unfollow')

    # Follow one or more extra user:
    extra_user = promo_settings['extra_user']
    if extra_user:
        for n in extra_user:
            if n not in users_to_unfollow:
                instagram_bot.follow_user(n)
                db.add_user(post_user, 'to_unfollow')

    # Follow the list of followers of the poster
    # Or if different rule, change 'post_user' to 'extra_user'
    if follow_users_user:
        users_to_follow = instagram_bot.get_follow_list(
            post_user, which_list='following')
        instagram_bot.follow_people(users_to_follow)
        for n in users_to_follow:
            db.add_user(n, 'to_unfollow')

    # Need to go back to post page after bouncing around users pages
    instagram_bot.go_to_post(post_url)
    print(f"Start running at: {datetime.datetime.now()}.")
    print(f"There are currently {len(user_list_in_db)} users to be mentioned.")

    if not combine_users:
        combine_users = 1

    comment_qnt = 0
    while len(user_list) >= combine_users:
        comment = ""
        for n in range(combine_users):
            comment += f"@{user_list[n]} "
            instagram_bot.comment_post(comment)
            rm_user = user_list.pop(0)
            db.delete_user(rm_user, 'followers')
            comment_qnt += 1
            print(f"#{comment_qnt}: {comment}")

        if comment_qnt < mentions:
            if comment_qnt % 5 == 0:
                action = random.randint(0,3)
                instagram_bot.random_action(action)
            if comment_qnt % 10 == 0:
                sleep(random.randint(45, 60))

        sleep(random.randint(10,15))

    instagram_bot.end_session()

    t_end = datetime.datetime.now()
    elapsed = (t_end - t_start).total_seconds()
    elapsed_formatted = time.strftime("%M:%S", time.gmtime(elapsed))
    print(f"A total of {comment_qnt} comments were done.")
    print(f"{len(user_list_in_db)-comment_qnt} users left to be mentioned.")
    print(f"-" * 50 + "\nIt took a total of {elapsed_formatted} minutes to run.")
    print("-" * 50 + "\nGood luck!\n" + "-" * 50)
    print(f"Last run at: {datetime.datetime.now()}.")


if __name__ == '__main__':
    # Settings of the promo share are available in "settings-promo.json":

    data = None
    settings = sys.argv[1]
    settings_path = os.path.join(os.getcwd(), settings)

    with open(settings_path, 'r') as f:
        data = f.read()
    obj = json.loads(data)
    promo_settings = obj['promo_settings']

    main(promo_settings)
    # TO DO:
    # Include an action to unfollow users after promoshare has ended
