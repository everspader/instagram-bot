import datetime
import random
import requests
import re
import traceback
from time import sleep

from instaloader import Instaloader, Profile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, ElementNotInteractableException)

from bot.db_handler import DbHandler


class InstagramBot():
    """
    Actual bot instance and all its methods corresponding to all
    the actions (or group of actions) that the bot will be able
    to perform.
    """
    def __init__(self, mode=None):
        self.chrome_options = webdriver.ChromeOptions()
        if mode != None:
            self.chrome_options.add_argument(mode)
        self.chrome_options.add_experimental_option(
            'prefs', {'intl.accept_languages': 'en,en_US'})
        self.webdriver = webdriver.Chrome(options=self.chrome_options)

    def login(self, username, password):
        """Get the username and password, input in the fields and login"""

        self.username = username
        self.password = password
        self.webdriver.get('https://www.instagram.com/')
        print("Redirecting to Instagram's Log In page...")
        sleep(random.randint(4,7))
        username_input = self.webdriver.find_element_by_name("username")
        password_input = self.webdriver.find_element_by_name("password")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        print("Login successful!")
        sleep(random.randint(4,7))
        self.skip_dialogs()
        print("-" * 50)

    def skip_dialogs(self):
        """
        Skip dialog messages asking to save info of login session
        and disable notifications for desktop.
        """

        try:
            save_info_button = self.webdriver.find_element_by_xpath(
                "//*[text()='Not Now']")
            save_info_button.click()
            print("Skipping save info pop up alert.")
            sleep(random.randint(1,5))
        except:
            pass

        try:
            notification_button = self.webdriver.find_element_by_xpath("//*[text()='Not Now']")
            notification_button.click()
            print("Skipping enable notifications alert.")
            sleep(random.randint(1,5))
        except:
            pass

    def follow_user(self, username):
        """Start following a user given its username"""

        self.webdriver.get(f"https://www.instagram.com/{username}")
        sleep(random.randint(2,5))

        buttons = self.webdriver.find_elements_by_css_selector('button')
        try:
            for n in buttons:
                if n.text in ["Follow Back", "Follow"]:
                    follow_button = n
                    follow_button.click()
                    print(f"You are now following {username}.")
                    sleep(random.randint(2,5))
                    return
        except:
            return
        else:
            print(f"{username} is already being followed.")
            return

    def unfollow_user(self, username):
        """Unfollow a user provided its username"""

        try:
            self.webdriver.get(f"https://www.instagram.com/{username}")
            sleep(3)
            try:
                unfollow_xpath = "button span[aria-label='Following']"
                unfollow_element = self.webdriver.find_element_by_css_selector(unfollow_xpath)
                unfollow_element.click()
                sleep(random.randint(1,4))

                try:
                    unfollow_confirm_xpath = "//*[text()='Unfollow']"
                    unfollow_confirm_element = self.webdriver.find_element_by_xpath(unfollow_confirm_xpath)
                    if unfollow_confirm_element.text == "Unfollow":
                        unfollow_confirm_element.click()
                        sleep(random.randint(1,4))
                        print(f"@{username} unfollowed.")
                except NoSuchElementException:
                    print("Could not find confirm unfollow button.")
                    return

            except NoSuchElementException:
                print(
                    f"Could not find unfollow button on {username}'s page. Maybe you don't "
                    "follow this user.")
                pass
        except:
            print(f"{username}'s profile not found.")
            return

    def follow_user_on_post(self, post_url=None):
        """Start following the publisher of a given post"""

        current_url = self.webdriver.current_url
        if post_url:
            self.go_to_post(post_url)
        elif "instagram.com/p/" not in current_url:
            print("An URL to a post must be provided.")
            return

        try:
            buttons = self.webdriver.find_elements_by_css_selector('button')
            username_url = self.webdriver.find_element_by_css_selector('a[href]')
            username = username_url.get_attribute("href").split('/')[-2]
            for n in buttons:
                if n.text in ["Follow"]:
                    follow_button = n
                    follow_button.click()
                    print("-" * 50 + f"\nYou are now following {username}.\n" +"-" * 50)
                    sleep(random.randint(2,5))
                    return
        except:
            print(f"{username} is already being followed.")
            return

    def go_to_post(self, post_url):
        """Helper function to redirect to a post's page"""

        try:
            self.webdriver.get(post_url)
            sleep(random.randint(6, 10))
        except:
            print(f"Missing post URL info.")
            raise

    def like_post(self, post_url=None):
        """
        Like a currently loaded post or visit a post from the
        link_post provided
        """

        current_url = self.webdriver.current_url
        if post_url:
            self.go_to_post(post_url)
        elif "instagram.com/p/" not in current_url:
            print("An URL to a post must be provided.")
            return

        try:
            button_like = self.webdriver.find_element_by_css_selector(
                "svg[aria-label='Like']")
            button_like.click()
            print("-" * 50 + "\nPost liked.\n" + "-" * 50)
        except NoSuchElementException:
            print("Could not find like button. Post not liked.")

        return

    def comment_post(self, comment, post_url=None):
        """Post a given comment to a post given its URL"""

        current_url = self.webdriver.current_url
        if post_url:
            self.go_to_post(post_url)
        elif "instagram.com/p/" not in current_url:
            print("An URL to a post must be provided.")
            return

        try:
            comment_box = self.webdriver.find_element_by_css_selector(
                "button svg[aria-label='Comment']")
            comment_box.click()
            sleep(random.randint(1,3))
            comment_box = self.webdriver.find_element_by_css_selector(
                "form textarea")
            comment_box.send_keys(comment)
            sleep(random.randint(2,4))
            try:
                comment_post = self.webdriver.find_element_by_css_selector(
                    "button[type='submit']")
                if comment_post.text == "Post":
                    comment_post.click()
                    sleep(random.randint(2,5))
                    # After a while Instagram seems to make it harder and harder to post
                    # multiple sequential comments. The comment box is locked for interaction,
                    # so after clicking on post the comment, it will check if the comment box
                    # is clickable, this means that the comment went through, otherwhise it's not.
                    try:
                        comment_box.click()
                        return
                    except ElementNotInteractableException:
                        print("Could not post comment")
                        raise

            except NoSuchElementException:
                print("Could not send comment to post. Element not found.")
                raise
        except ElementNotInteractableException:
            print("Could not write comment to post. Element not interactable.")
            raise
        except TimeoutException as exception:
            self.webdriver.get(self.webdriver.current_url)
            raise exception
        except NoSuchElementException:
            print("Could not write comment to post. Element not found.")
            raise

    def get_username_from_post(self, post_url=None):
        """Get the username of the post publisher"""

        current_url = self.webdriver.current_url
        if post_url:
            self.go_to_post(post_url)
        elif "instagram.com/p/" not in current_url:
            print("An URL to a post must be provided.")
            return

        try:
            username_url = self.webdriver.find_element_by_css_selector('a[href]')
            username = username_url.get_attribute("href").split('/')[-2]
            return username
        except NoSuchElementException:
            print("Couldn't find username of the poster.")
            return

    def get_like_list_from_post(self, post):
        """Retrieve the list of users that liked a post"""
        pass

    def unfollow_people(self, people):
        """
        Unfollow a list of given usernames that were added to the
        the database
        """
        if not isinstance(people, (list,)):
            p = people
            people = []
            people.append(p)

        db = DbHandler()

        print(f"{len(people)} users to be unfollowed.\n" + "-" * 50)
        k = 0

        for user in people:
            try:
                self.unfollow_user(user)
                db.delete_user(self.username, user, 'followers')
                k+=1
                print(f"@{user} deleted from db. ({k}/{len(people)})\n" + "-" * 50)
            except:
                traceback.print_exc()

    def follow_people(self, people, store=None):
        """Follow a list of users and save them in db (optional)"""

        if not isinstance(people, (list,)):
            p = people
            people = []
            people.append(p)

        print(f"{len(people)} users to be followed.\n" + "-" * 50)

        if store is not None:
            db = DbHandler()

        k = 0
        for user in people:
            try:
                self.follow_user(user)
                if store:
                    db.add_user(self.username, user, 'followers')
                k+=1
                print(f"Now following: @{user}. ({k}/{len(people)})\n" + "-" * 50)
            except:
                traceback.print_exc()

    def get_number_follow(self, username=None, which_list="following"):
        """
        Alternative method to scrap the list of followers or followees
        from a user using the Selenium package. Takes longer times.
        This method should be ignored. It's kept here as an example of
        how to use Selenium for this action.
        """

        if username is None:
            username = self.get_username_from_post()

        url = f'https://www.instagram.com/{username}'
        r = requests.get(url).text
        if which_list == "followers":
            number_follow = re.search('"edge_followed_by":{"count":([0-9]+)}',r).group(1)
        else:
            number_follow = re.search('"edge_follow":{"count":([0-9]+)}',r).group(1)

        return int(number_follow)

    def get_follow_list(self, username=None, which_list="following", amount=None):
        """
        Get the complete list or a specific amount of followers or followees of
        a user using instaloader package.
        """

        # Interesting to measure how long a list takes to be retrieved
        t_start = datetime.datetime.now()
        L = Instaloader()
        L.login(self.username, self.password)

        if username is None:
            username = self.username

        profile = Profile.from_username(L.context, username)

        if which_list == "following":
            follow_node = profile.get_followees()
        elif which_list == "followers":
            follow_node = profile.get_followers()

        follow = [f.username for f in follow_node]
        if amount:
            follow = random.sample(follow, amount)

        t_end = datetime.datetime.now()
        elapsed = (t_end - t_start).total_seconds()
        print(
            f"It took {elapsed} seconds to retrieve the list "
            f"of {len(follow)} {which_list}\n" + "-" * 50)

        return follow

    def unfollow_new_followed_list(self):
        """
        Very specific method to be used when many users were followed
        as part of a strategy to increase interactions. These users shall
        be unfollowed after some time set in the settings.
        """

        print("Checking for users to unfollow...")
        db = DbHandler()
        unfollow_users = db.get_unfollow_list(self.username, 'followers')

        if len(unfollow_users) == 0:
            print("No new users to unfollow.\n" + "-" * 50)
        elif len(unfollow_users) > 0:
            print(f"{len(unfollow_users)} new users will be unfollowed...")
            self.unfollow_people(unfollow_users)
            print("-" * 50)
        return

    def follow_people_from_hashtags(self, hashtags,
                                    interactions=10, likes_over=500):
        """
        Navigate to the spcific hashtag page and perform a given number
        of interactions. An interaction is defined by liking a post and
        following the user provided that the post is not over a likes
        limit.
        """
        # This method was initially developed as a collection of actions
        # to increase interactions via hashtags. It was never officially
        # used but it will be maintained for possible future applications.

        db = DbHandler()
        prev_user_list = db.get_followed_list(self.username, 'followers')
        new_followed = []
        followed = 0
        new_likes = 0

        for hashtag in hashtags:
            print(f"Redirecting to tags page for: \"#{hashtag}\"\n" + "-" * 50)
            self.webdriver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            sleep(5)
            first_thumbnail = self.webdriver.find_element_by_css_selector(
                "a[href]")
            first_thumbnail.click()
            sleep(3)

            try:
                while new_likes < interactions:
                    t_start = datetime.datetime.now()
                    username = self.get_username_from_post()
                    likes_over_limit = False
                    try:
                        elements = self.webdriver.find_elements_by_css_selector(
                            "button[type='button'] span")
                        likes = int([n.text for n in elements if n.text != ""][0])
                        if likes > likes_over:
                            print(f"{username}'s post has over {likes_over} likes.\n" + "-" * 50)
                            likes_over_limit = True
                            self.webdriver.find_element_by_link_text('Next').click()
                            sleep(3)
                            continue
                    # Exception in case there's no likes in a post yest
                    except NoSuchElementException:
                        print(f"Unable to find number of likes in {username}'s post.")
                        continue

                    try:
                        if username not in prev_user_list and not likes_over_limit:
                            print(f"Looking at {username}'s post...")
                            self.follow_user_on_post()
                            db.add_user(self.username, username, 'followers')
                            followed += 1
                            print(f"Followed: @{username}, #{followed}")
                            new_followed.append(username)
                            self.like_post()
                            likes += 1
                            new_likes += 1
                            print(f"Liked @{username}'s post: {likes} likes\n" + "-" * 50)
                            sleep(3)
                        else:
                            print(f"Already following @{username}.\n" + "-" * 50)

                    except:
                        traceback.print_exc()
                        continue

                    self.webdriver.find_element_by_link_text('Next').click()
                    sleep(random.randint(2,5))

                t_end = datetime.datetime.now()

                t_elapsed = t_end - t_start
                print(f"This hashtag took {t_elapsed} seconds")

            except:
                traceback.print_exc()
                continue

            prev_user_list.append(username)

            print(f"Liked {new_likes} photos with the hashtag #{hashtag}")
            print(f"Following {followed} new users")

        return new_followed

    def random_scroll(self):
        """Attempt to fake a scroll down+up human action"""

        scroll_times = int(random.random() * 5)
        scroll_current = 0
        for _ in range(scroll_times):
            scroll_dist = int(random.random() * 500)
            scroll_current = scroll_current + scroll_dist
            self.webdriver.execute_script(f"window.scrollTo(0, {scroll_current})")
        self.webdriver.execute_script(f"window.scrollTo(0, 0)")
        sleep(random.randint(2,4))

    def random_action(self, action, post_url=None):
        """
        Define some random actions to perform every now and then
        on an attempt to trick Instagram
        """
        # Action 0 (not imp): Go to own feed and scroll
        # Action 1 (not imp): Like a random post from the same page
        # Action 2: Comment on a random post from the same page
        # Action 3: Go to another random page do something and come back
        if post_url is None:
            post_url = self.webdriver.current_url
        if action == 0:
            pass
        if action == 1:
            pass
        else:
            link_list = self.webdriver.find_elements_by_css_selector("a[href*='/p/']")
            post_links = [n.get_attribute('href') for n in link_list]
            thumbnails = [n for n in post_links if '/c/' not in n and n != post_url]
            post = thumbnails[random.randint(0,len(thumbnails)-1)]
            print("-" * 50 + "\nRedirecting to some other post\n" + "-" * 50)
            self.go_to_post(post)
            self.random_scroll()
            if action == 2:
                self.like_post()
            # Go back to post
            print("-" * 50 + "\nGoing back to original post\n" + "-" * 50)
            self.go_to_post(post_url)
            return

    def end_session(self):
        """Close browser and terminate session"""
        self.webdriver.close()

    def __exit__(self, exc_type, exc_value):
        self.end_session()
