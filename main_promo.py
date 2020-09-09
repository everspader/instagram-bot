import datetime
import random
from time import sleep

import constants
from db_handler import DbHandler
from bot import InstagramBot


username = constants.INST_USER
password = constants.INST_PASS

post_link = 'https://www.instagram.com/p/CDZsXbvpdxI/'

instagram_bot = InstagramBot(username, password)
instagram_bot.login()

breakpoint()
print("Redirecting to...")
print(f"{post_link}")
print("-" * 50)

# user_list = instagram_bot.get_follow_list(which_list='following', 10)
#Number of users to be combined in the comments
combine_users = 4

while len(user_list) >= combine_users:
    comment = ""
    for n in range(combine_users):
        user_n = user_list[n]
        comment += f"@{user_n} "
    rm_one_user = user_list.pop(0)

    instagram_bot.comment_post(post_link, comment)
    sleep(random.randint(5,7))

    #include follow user function
    #include like post function