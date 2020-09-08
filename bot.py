import datetime
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from db_handler import DbHandler

class InstagramBot():
    """
    Class containing objects from Instagram's login page. Safe method
    in case the names of the page objects change over time
    """
    def __init__(self, username, password):
        self.webdriver_profile = webdriver.ChromeOptions()
        self.webdriver_profile.add_experimental_option(
            'prefs', {'intl.accept_languages': 'en,en_US'})
        self.webdriver = webdriver.Chrome()
        self.username = username
        self.password = password

    def login(self):
        """Get the username and password, input in the fields and login"""

        self.webdriver.get('https://www.instagram.com/')
        print("Redirecting to Instagram's Log In page...")
        sleep(5)
        username_input = self.webdriver.find_element_by_name("username")
        password_input = self.webdriver.find_element_by_name("password")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        # login_button = self.webdriver.find_element_by_xpath(
        #     "//*[@id='loginForm']/div/div[3]/button/div")
        # login_button.click()
        print("Login successful!")
        sleep(5)
        self.skip_dialogs()
        print("-" * 50)

    def skip_dialogs(self):
        """
        Skip dialog messages asking to save info of login session
        and disable notifications for desktop.
        """
        try:
            save_info_button = self.webdriver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/div/div/div/button")
            save_info_button.click()
            print("Skipping save info pop up alert.")
            sleep(2)
        except:
            pass

        try:
            notificaiton_button = self.webdriver.find_element_by_xpath(
                "/html/body/div[4]/div/div/div/div[3]/button[2]")
            notificaiton_button.click()
            print("Skipping enable notifications alert.")
            sleep(2)
        except:
            pass

    def go_to_hashtags_pages(self, hashtag):
        """
        Navigate to the hashtag pages to interact with posts
        os a specific hashtag.
        """
        self.webdriver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        sleep(5)

    def follow_user(self, username):
        """Follow a user provided its username"""
        # add to database
        pass

    def get_follow_list(self, username=None,
                           which_list='followers', amount=10):
        """
        Scrap off either the list of followers or following users,
        from a specific username depending on the parameter set on
        which_list. And return a given number in case there are too
        many. If username not provided then retrieve list of followers
        of the user that is logged in the session.
        """
        if username == None:
            username = self.username
        if which_list == 'followers':
            list_item = 0
        elif which_list == 'following':
            list_item = 1

        self.webdriver.get(f"https://www.instagram.com/{username}")
        follow_link = self.webdriver.find_elements_by_css_selector('ul li a')[list_item]
        follow_link.click()
        sleep(2)
        follow_list = self.webdriver.find_element_by_css_selector("div[role='dialog'] ul")
        number_follow = len(follow_list.find_elements_by_css_selector("li"))

        follow_list.click()
        action_chain = webdriver.ActionChains(self.webdriver)
        while (number_follow) < amount:
            action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            number_follow = len(follow_list.find_elements_by_css_selector("li"))
            print(number_follow)

        follow = []
        for user in follow_list.find_elements_by_css_selector("li"):
            user_link = user.find_element_by_css_selector('a').get_attribute("href")
            user_name = user_link.split('/')[-2]
            print(user_name)
            follow.append(user_name)
            if len(follow) == amount:
                break

        return follow

    def get_number_of_followers(self, username):
        """Retrieve the number of followers from an user"""
        pass

    def unfollow_new_followed_list(self):
        """
        Check if there are users that should be unfollowed and start
        unfollowing them one by one.
        """
        print("Checking for users to unfollow...")
        db = DbHandler()
        unfollow_users = db.get_unfollow_list()

        if len(unfollow_users) == 0:
            print("No new users to unfollow.")
        elif len(unfollow_users) > 0:
            print(f"{len(unfollow_users)} new users will be unfollowed...")
            self.unfollow_people(unfollow_users)

    def unfollow_user(self, username):
        """Unfollow a user provided its username"""
        try:
            self.webdriver.get(f"https://www.instagram.com/{user}")
            sleep(3)
            try:
                unfollow_xpath = (
                    "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button")
                unfollow_element = self.webdriver.find_element_by_xpath(unfollow_xpath)
                unfollow_element.click()

                try:
                    unfollow_confirm_xpath = "/html/body/div[4]/div/div/div/div[3]/button[1]"
                    unfollow_confirm_element = self.webdriver.find_element_by_xpath(unfollow_confirm_xpath)
                    if unfollow_confirm_element.text == "Unfollow":
                        unfollow_confirm_element.click()
                        sleep(3)
                        print(f"{user} unfollowed.")
                        # db.delete_user(user)
                        # db_users.delete_user(user)
                        # print(f"{user} deleted from db")
                except NoSuchElementException:
                    print("Could not find confirm unfollow button.")
                    # return exception
                    pass

            except NoSuchElementException:
                print(
                    f"Could not find unfollow button on {user}'s page. Maybe you don't "
                    "follow this user.")
                # db.delete_user(user)
                # print(f"{user} deleted from db")
                # return exception
                pass
        except:
            traceback.print_exc()
            # return exception
            pass

    def unfollow_people(self, people):
        """
        Unfollow new users based on the date that they were added
        to the database and according to the number of days that
        they should be kept as stated in the settings.
        """
        if not isinstance(people, (list,)):
            p = people
            people = []
            people.append(p)

        db = DbHandler()

        for user in people:
            try:
                self.unfollow_user(user)
            except:
                pass
            db.delete_user(user)
            print(f"{user} deleted from db")

    def end_session(self):
        """Close browser and terminate session"""
        self.webdriver.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_session()


    def follow_people(self, hashtags, interactions=10):
        db = DbHandler()
        prev_user_list = db.get_followed_list()
        new_followed = []
        followed = 0
        new_likes = 0

        for hashtag in hashtags:
            self.webdriver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            sleep(5)

            first_thumbnail = self.webdriver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/article/div[1]/div/div/div[1]/div[1]")
            first_thumbnail.click()
            sleep(random.randint(1, 3))

            try:
                for x in range(1, interactions):
                    t_start = datetime.datetime.now()
                    username = self.webdriver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                    likes_over_limit = False
                    try:
                        likes_raw = self.webdriver.find_element_by_xpath(
                            '/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div/button/span').text
                        breakpoint()
                        likes = int(likes_raw.replace(',',''))
                        if likes > constants.LIKES_OVER:
                            print(f"likes over {constants.LIKES_OVER}")
                            likes_over_limit = True
                    # Exception in case there's no likes in a post yest
                    except NoSuchElementException:
                        pass

                    try:
                        print(f"Detected: {username}")
                        if username not in prev_user_list and not likes_over_limit:
                            follow_button = '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button'
                            if self.webdriver.find_element_by_xpath(follow_button).text == 'Follow':
                                db.add_user(username)
                                self.webdriver.find_element_by_xpath(follow_button).click()
                                followed += 1
                                print(f"Followed: {username}, #{followed}")
                                new_followed.append(username)

                            button_like = self.webdriver.find_element_by_xpath(
                                "/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button")
                            button_like.click()
                            likes += 1
                            new_likes += 1
                            print(f"Liked {username}'s post: {likes} likes")
                            # sleep(random.randint(5, 18))
                            sleep(3)

                        self.webdriver.find_element_by_link_text('Next').click()
                        # sleep(random.randint(20, 30))
                        sleep(3)

                    except:
                        traceback.print_exc()
                        continue

                t_end = datetime.datetime.now()

                t_elapsed = t_end - t_start
                print(f"This post took {t_elapsed} seconds")

            except:
                traceback.print_exc()
                continue

            for n in range(0, len(new_followed)):
                prev_user_list.append(new_followed[n])

            print(f"Liked {new_likes} photos with the hashtag #{hashtag}")
            print(f"Following {followed} new users")