## INSTAGRAM BOT WITH PYTHON AND SELENIUM 🤖

This is a simple Instagram bot created with Python 3.8 and Selenium webdriver for educational purposes only.\
The concept behind the bot is to use Selenium webdriver to simulate the actions of a user acessing Instagram's website via the browser to interact with posts by commenting and liking and user's pages by following or unfollowing them.\

So far the interactions already implemented are:
* Follow/unfollow users form their profile pages;
* Follow/unfollow a list of people
* Follow user directly on a post;
* Redirect to any post;
* Like post;
* Comment post;
* Retrieve username from post's page;
* Get number of followers/followees;
* Get complete or partial list of followers/followees
* Unfollow a list of people given a time window after being followed
* Visiting a given hashtag's page to:
  * Like `n` posts with less than a given number of likes and follow the users
* Store the newly followed users in a database for `n` days
* Random action from the listed above to simulate a human aciton
* More to come...

*Disclaimer: this bot is intended solely for educational purposes involving Python and Selenium. It was not meant to be an unethical way to leverage from social media interactions and gain social status*

### Starting with Selenium Webdriver

Install the correct Selenium webdriver for your browser. If you want to user Google Chrome, download [chromedriver](https://chromedriver.chromium.org/downloads) or download [geckodriver](https://github.com/mozilla/geckodriver/releases) for Mozilla Firefox.\
After downloading the specific webdriver, it's best if you keep it in your local `$PATH`.

If you don't know where to find your `$PATH`, simply open a terminal window and run `echo $PATH`. It's usually `/usr/bin` or `/usr/local/bin`.

Now to move the downloaded driver to the correct location just run the following command:
```
mv ~/Downloads/chromedriver /usr/local/bin
```
(Make sure to replace the source location with yours and change `chromedriver` to `geckodriver` if you're running on Firefox).\
Now, to make sure, go the folder and check that the file is there. Do so by running these commands:
```
cd /usr/local/bin
ls
```
### Setting Up PostgreSQL Database and Table

You will need a table to store the data of the new users that your bot starts to follow and when it happened so it will know when to unfollow them (after a specific number of days).\
You can use any database of your preference but I chose to use PostgreSQL.\
I'm assuming that you already have PostgreSQL installed and running smoothly in your computer. If you don't go to PostgreSQL's [ website](https://www.postgresql.org/download/), download it and install it. Then you can easily find a tutorial on how to set it up properly for your OS.
Lastly, all you have to do is start the Postgres server, create a database and a table.
* Start Postgres Server:
```shell
pg_ctl -D /usr/local/var/postgres start
```
* Create Database (and call it whatever you want):
```shell
createdb instabot
```
* Enter the database:
```shell
psql instabot
```
* Create a table for the users to follow:
```shell
CREATE TABLE IF NOT EXISTS followers (
    username VARCHAR(50),
    date_added TIMESTAMP,
    account VARCHAR(50)
);
```
and one for the users that should be unfollowed:
```shell
CREATE TABLE IF NOT EXISTS to_unfollow (
    username VARCHAR(50),
    date_added TIMESTAMP,
    account VARCHAR(50)
);
```
And you are all set with your database.

### Project Setup

Assuming you have your database set up and you have already cloned this repository, begin by installing the Python package dependencies by running:
```shell
pip install -r requirements.txt
```
Now you need to insert some information in the file `settings-prod.json`, such as you're Instagram username and password, database username (and password if any) and name that you passed on the steps above.
Here you can also pass other settings for the bot, such as a list of the hashtags you want it to interact with, an upper limit of the number of likes of a post to interact with and so on.\

### Using the Bot

From here on you can use your creativity to write a script to use the bot and all its methods to perform actions as you wish. Just be mindful of how you use it to not have you Instagram account being banned by Instagram itself.

#### Usage Example 1:

In `main.py` you will find a simple script that will play around with your predefined list of hashtags, go into each of its page and start liking posts and following users.

Hoping that you will start getting some interactions back, the users your bot followed will be stored in a database and will be unfollowed when you run your bot again (after the giving number of days before unfollowing).

Assuming you already have your `settings-prod.json` configured, just execute the following command to run the script:
```shell
python main.py settings-prod.json
```

#### Usage Example 2:

`main_promo.py` is a script that can be used to participate in almost any giveaway post that users create on Instagram requiring you to like the post, follow users and tag some friends in order to enter a raffle to win something.

All you have to do here is edit the settings in `settings-promo-prod.json` as follows:
* **post_url**: Actual url of the post
* **user_list**: List of users to be mentioned. If can be either `followers`, `following`. If empty it defaults to `followers`,
* **combine_users**: when it's required to mention more than one person at a time, set the number here. Otherwise `false`.
* **like_post**: `true` or `false` for liking the post.
* **follow_user**: `true` or `false` for following the post's publisher.
* **follow_users_user**: `true` or `false` to follow the list of followers of the post's publisher.
* **extra_user**: List of extra users that should be followed.
* **user**: Which account should the list of users to be mentioned be retrieved from (you might run the bot with your account but get the users list from another).
* **mentions**: Limit of mentions for every time the script is run. This is a limit to avoid Instagram from blocking your account from using it.
* **end_promo**: Date and time that the giveaway will end as a timestamp format.

After both `settings-*.json` files are configured, you can put the bot to work for you by running the script as follows:
```shell
python main_promo.py settings-prod.json settings-promo-prod.json
```

As you might have realized, running the above command will only run the script once and tag a number of people equal to the value set for mentions in settings. What you could do is create a shell script that runs the command and set a `cronjob` to run it periodically. In my personal experience running every 30 minutes continuously will not put you under Instagram's radar.


### To do:

- Add tests
- Deploy somewhere so other non-IT people can make use of it in a more simple fashion.