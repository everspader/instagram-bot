from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

    def unfollow_user(self, username):
        """Unfollow a user provided its username"""
        # remove from database
        pass

    def end_session(self):
        """Close browser and terminate session"""
        self.webdriver.close()

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

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_session()
