import json
import os

global INST_USER, INST_PASS
global DB_USER, DB_HOST, DB_PASS, DB_NAME
global DAYS_TO_UNFOLLOW, HASHTAGS, LIKES_OVER, CHECK_FOLLOWERS_EVERY

data = None
settings = "settings-test.json"

settings_path = os.path.join(os.getcwd(), settings)

with open(settings_path, 'r') as f:
    data = f.read()
obj = json.loads(data)
INST_USER = obj['instagram']['username']
INST_PASS = obj['instagram']['password']
DB_USER = obj['db']['user']
DB_HOST = obj['db']['host']
DB_PASS = obj['db']['pass']
DB_NAME = obj['db']['database']

DAYS_TO_UNFOLLOW = obj['config']['days_to_unfollow']
LIKES_OVER = obj['config']['likes_over']
CHECK_FOLLOWERS_EVERY = obj['config']['check_followers_every']
HASHTAGS = obj['config']['hashtags']
