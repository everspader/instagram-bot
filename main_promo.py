import datetime
import random
from time import sleep

from bot import constants, InstagramBot, DbHandler


username = constants.INST_USER
password = constants.INST_PASS

instagram_bot = InstagramBot(username, password)
instagram_bot.login()

promo_settings = {
     "post_url": "",
     "user_list": user_list,
     "combine_users": 2,
     "like_post": True,
     "follow_user": True,
}

if not user_list:
    user_list = instagram_bot.get_follow_list(which_list='following', amount=10)

# Convert dict pairs keys,items into variables
locals().update(promo_settings)

try:
    instagram_bot.go_to_post(post_url=post_url)
except:
    print("You must provide the URL to the post.")

if like_post:
    instagram_bot.like_post()
if follow_user:
    instagram_bot.follow_user_on_post()
if not combine_users:
    combine_users = 1

comment_combinations = 0
while len(user_list) >= combine_users:
    comment = ""
    for n in range(combine_users):
        user_n = user_list[n]
        comment += f"@{user_n} "
    rm_one_user = user_list.pop(0)

    instagram_bot.comment_post(comment)
    comment_combinations += 1
    sleep(random.randint(3,5))

instagram_bot.end_session()
