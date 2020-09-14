import datetime
import json
import os
import random
import sys
from time import sleep

from bot import constants, InstagramBot, DbHandler


def main(promo_settings):
    """
    Main function to run a promoshare on a specific post according
    to predefined settings.
    """
    t_start = datetime.datetime.now()

    # BOT INITIALIZATION
    username = constants.INST_USER
    password = constants.INST_PASS

    instagram_bot = InstagramBot(username, password)
    instagram_bot.login()

    db = DbHandler()
    user_list_in_db = db.get_followed_list('followers')

    user = promo_settings['user']
    if not user:
        user = constants.INST_USER

    # If no users are registered in db, then retrieve a specific list of users
    # from the specified user's profile and add them to db.
    if not user_list_in_db:
        user_list = instagram_bot.get_follow_list(
            user, which_list='followers')
        for u in user_list:
            db.add_user(u, 'followers')

    post_url = promo_settings['post_url']
    like_post = promo_settings['like_post']
    combine_users = promo_settings['combine_users']
    follow_user = promo_settings['follow_user']
    follow_users_user = promo_settings['follow_users_user']
    mentions = promo_settings['mentions']

    # From the users in the database, get a small random sample to
    # avoid Instagram blocking
    user_list = random.sample(user_list_in_db, mentions)
    # BEGIN OF BOT ACTIONS:
    try:
        instagram_bot.go_to_post(post_url)
    except:
        print("You must provide the URL to the post.")
        return

    users_to_unfollow = []
    if like_post:
        instagram_bot.like_post()
    post_user = instagram_bot.get_username_from_post()
    if follow_user and post_user not in user_list_in_db:
        instagram_bot.follow_user_on_post()
        users_to_unfollow.append(post_user)
    if not combine_users:
        combine_users = 1
    # Follow an extra user:
    extra_user = promo_settings['extra_user']
    if extra_user:
        for n in extra_user:
            if extra_user not in user_list_in_db:
                instagram_bot.follow_user(n)
                users_to_unfollow.append(n)

    # Follow the list of followers of the poster
    # Or if different rule, change 'post_user' to 'extra_user'
    if follow_users_user:
        users_to_follow = instagram_bot.get_follow_list(
            post_user, which_list='following')
        instagram_bot.follow_people(users_to_follow)
        [users_to_unfollow.append(n) for n in users_to_follow]

    # Need to go back to post page after bouncing around users pages
    instagram_bot.go_to_post(post_url)
    print(f"There are currently {len(user_list_in_db)} users to be mentioned.")

    comment_qnt = 0
    while len(user_list) >= combine_users:
        comment = ""
        for n in range(combine_users):
            comment += f"@{user_list[n]} "

        try:
            instagram_bot.comment_post(comment)
            rm_user = user_list.pop(0)
            db.delete_user(rm_user, 'followers')
            comment_qnt += 1
            print(f"#{comment_qnt}: {comment}")
        finally:
            if comment_qnt < mentions:
                if comment_qnt % 5== 0:
                    instagram_bot.human_action()
                if comment_qnt % 10 == 0:
                    sleep(random.randint(45, 60))

        sleep(random.randint(10,15))

    instagram_bot.end_session()

    t_end = datetime.datetime.now()
    elapsed = (t_end - t_start).total_seconds()
    print("-" * 50)
    print(f"It took a total of {int(elapsed/60)}:{elapsed%60} minutes to run.")
    print(f"A total of {comment_qnt} comments were done.")
    print(f"{len(user_list_in_db)-comment_qnt} users left to be mentioned.")
    print("-" * 50)
    print("Good luck!")
    print("-" * 50)
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
