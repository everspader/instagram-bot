import datetime
from time import sleep

import constants
from db_handler import DbHandler
from bot import InstagramBot


username = constants.INST_USER
password = constants.INST_PASS
# hashtags = constants.HASHTAGS
# likes_over = constants.LIKES_OVER
# check_followers_every = constants.CHECK_FOLLOWERS_EVERY
# days_to_unfollow = constants.DAYS_TO_UNFOLLOW

post_link = 'https://www.instagram.com/p/CDZsXbvpdxI/'

# start = datetime.datetime.now()

instagram_bot = InstagramBot(username, password)
instagram_bot.login()

print("Redirecting to...")
print(f"{post_link}")
print("-" * 50)
comment = "Hello, I'm your Bot friend."
instagram_bot.comment_post(post_link, comment)
