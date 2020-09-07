import datetime
import traceback
import random
from time import sleep

from selenium.common.exceptions import NoSuchElementException

import db_handler, constants, db_users
from login_page import LoginPage


def login(webdriver):
    """
    Initialize Instagram's page and input username and password to
    login and skip save info and notifications alerts.
    """
    login_page = LoginPage(webdriver)
    username = constants.INST_USER
    password = constants.INST_PASS
    login_page.login(username, password)
    login_page.skip_save_info()
    login_page.skip_notifications()


def follow_people(webdriver):
    prev_user_list = db_users.get_followed_users()
    new_followed = []
    followed = 0
    new_likes = 0

    for hashtag in constants.HASHTAGS:
        webdriver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        sleep(5)

        first_thumbnail = webdriver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/article/div[1]/div/div/div[1]/div[1]")
        first_thumbnail.click()
        sleep(random.randint(1, 3))

        try:
            for x in range(1,200):
                t_start = datetime.datetime.now()
                username = webdriver.find_element_by_xpath(
                    '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                likes_over_limit = False
                try:
                    likes_raw = webdriver.find_element_by_xpath(
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
                        if webdriver.find_element_by_xpath(follow_button).text == 'Follow':
                            db_users.add_user(username)
                            webdriver.find_element_by_xpath(follow_button).click()
                            followed += 1
                            print(f"Followed: {username}, #{followed}")
                            new_followed.append(username)

                        button_like = webdriver.find_element_by_xpath(
                            "/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button")
                        button_like.click()
                        likes += 1
                        new_likes += 1
                        print(f"Liked {username}'s post: {likes} likes")
                        # sleep(random.randint(5, 18))
                        sleep(3)

                    webdriver.find_element_by_link_text('Next').click()
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


def unfollow_people(webdriver, people):
    """
    Unfollow new users based on the date that they were added
    to the database and according to the number of days that
    they should be kept as stated in the settings.
    """
    if not isinstance(people, (list,)):
        p = people
        people = []
        people.append(p)

    for user in people:
        try:
            webdriver.get(f"https://www.instagram.com/{user}")
            sleep(3)
            try:
                unfollow_xpath = "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button"
                unfollow_element = webdriver.find_element_by_xpath(unfollow_xpath)
                unfollow_element.click()

                try:
                    unfollow_confirm_xpath = "/html/body/div[4]/div/div/div/div[3]/button[1]"
                    unfollow_confirm_element = webdriver.find_element_by_xpath(unfollow_confirm_xpath)
                    if unfollow_confirm_element.text == "Unfollow":
                        unfollow_confirm_element.click()
                        sleep(3)
                        print(f"{user} unfollowed.")
                        db_users.delete_user(user)
                        print(f"{user} deleted from db")
                except NoSuchElementException:
                    print("Could not find confirm unfollow button. Skipping to next user.")
                    continue

            except NoSuchElementException:
                print(
                    f"Could not find unfollow button on {user}'s page. Maybe you don't "
                    "follow this user. Skipping to next user.")
                db_users.delete_user(user)
                print(f"{user} deleted from db")
                continue
        except Exception:
            traceback.print_exc()
            continue
