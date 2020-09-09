## INSTAGRAM BOT WITH PYTHON AND SELENIUM

This is a simple Instagram bot created with Python 3.8 and Selenium webdriver for educational purposes only.\
The concept behind the bot is to use Selenium webdriver to simulate the actions of a user acessing Instagram's website via the browser to interact with posts and users pages.\
So far the interactions include:
* Like posts;
* Comment posts;
* Follow/Unfollow users from their pages;
* Follow users from a post's pages;
* Retrieve username from post's page;
* Visiting a given hashtag's page to:
  * Like `n` posts with less than a given number of likes and follow the users
* Store the newly followed users in a database for `n` days
* Unfollow a list of users;
* Scrap off the list of followers or following users from a given user.
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
I'm assuming that you already have PostgreSQL installed and running smoothly in your computer so all you have to do is start the Postgres server, create a database and a table.
* Start Postgres Server:
```
pg_ctl -D /usr/local/var/postgres start
```
* Create Database (and call it whatever you want):
```
createdb instabot
```
* Enter the database:
```
psql instabot
```
* Create a table:
```
CREATE TABLE followers (
    username VARCHAR,
    date_added DATE,
);
```
And you are all set with your database.

### Project Setup

Assuming you have your database set up and you have already cloned this repository, begin by installing the Python package dependencies by running:
```
pip install -r requirements.txt
```
Now you need to insert some information in the file `settings-prod.json`, such as you're Instagram username and password, database username and name (and password if any), and other settings for the bot, such as a list of the hashtags you want it to interact with, an upper limit of the number of likes of a post to interact with and so on.\
Next, in `constants.py` change the name of the file that is being read (`settings-local.json`) to the appropriate name of the `settings-*.json` file containing your data.\

### Running the Bot

In `main.py` you will find a simple script that will play around with your predefined list of hashtags, go into each of its page and start liking posts and following users.

Hoping that you will start getting some interactions back, the users your bot followed will be stored in a database and will be unfollowed when you run your bot again (after the giving number of days before unfollowing).

Now you can play around with the bot and all its methods and adapt it to your needs or reuse the same concepts to other applications.

### To do:

Deploy the project to a cloud service and have the option to run it autonomously according to users specification.