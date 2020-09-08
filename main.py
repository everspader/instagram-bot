from time import sleep

import constants
from bot import InstagramBot


# constants.init()
username = constants.INST_USER
password = constants.INST_PASS
hashtags = constants.HASHTAGS

instagram_bot = InstagramBot(username, password)
instagram_bot.login()

instagram_bot.unfollow_new_followed_list()
breakpoint()
# followers = instagram_bot.get_follow_list(which_list='following')
# breakpoint()
# for hashtag in hashtags:
#     instagram_bot.go_to_hashtags_pages(hashtags)
#     # do stuff
