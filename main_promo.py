import datetime
import random
from time import sleep

from bot import constants, InstagramBot


def main(post_url, promo_settings, user=None):

    user_list = None
    users_to_unfollow = []

    if user is None:
        user = constants.INST_USER

    # List of users to be tagged in comments (select amount):
    if not user_list:
        user_list = instagram_bot.get_follow_list(
            user, which_list='following', amount=20)

    # Convert dict pairs keys,items into variables
    locals().update(promo_settings)

    # BEGIN OF BOT ACTIONS:
    username = constants.INST_USER
    password = constants.INST_PASS

    instagram_bot = InstagramBot(username, password)
    instagram_bot.login()

    try:
        instagram_bot.go_to_post(post_url=post_url)
    except:
        print("You must provide the URL to the post.")
        return

    if like_post:
        instagram_bot.like_post()
    if follow_user:
        instagram_bot.follow_user_on_post()
        post_user = instagram_bot.get_username_from_post()
        users_to_unfollow.append(post_user)
    if not combine_users:
        combine_users = 1

    # Follow an extra user:
    extra_user = None
    if extra_user:
        instagram_bot.follow_user(extra_user)
        users_to_unfollow.append(post_user)

    # Follow the list of followers of the poster
    # Or if different rule, change 'post_user' to 'extra_user'
    if follow_users_user:
        post_user = instagram_bot.get_username_from_post()
        users_to_follow = instagram_bot.get_follow_list(
            post_user, which_list='following')
        instagram_bot.follow_people(users_to_follow, store=True)
        [users_to_unfollow.append(n) for n in users_to_follow]

    comment_qnt = 0
    # Need to go back to post page after bouncing around users pages
    instagram_bot.go_to_post(post_url)
    while len(user_list) >= combine_users:
        comment = ""
        for n in range(combine_users):
            user_n = user_list[n]
            comment += f"@{user_n} "
        rm_one_user = user_list.pop(0)

        instagram_bot.comment_post(comment)
        comment_qnt += 1
        sleep(random.randint(3,5))

    print(f"A total of {comment_qnt} comments were done.")
    print("-" * 50)
    print("Good luck!")

    instagram_bot.end_session()


if __name__ == '__main__':
    # Settings of the promo share:
    # combine_users: means how many users should be tagged per comment
    # follow_users_user: to follow poster followers

    # INSERT USERNAME FROM WHICH TO RETRIEVE A LIST OF USERS
    # TO BE TAGGED IN COMMENTS.

    user = "USERNAME"
    # INSERT THE URL OF THE POST CONTAINING THE PROMO
    post_url = "INSERT_POST_URL"

    promo_settings = {
        "post_url": post_url,
        "user_list": user_list,
        "combine_users": 1,
        "like_post": True,
        "follow_user": True,
        "follow_users_user": True
    }
    main(post_url, promo_settings, user)
