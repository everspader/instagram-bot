from time import sleep

class LoginPage:
    """
    Class containing objects from Instagram's login page. Safe method
    in case the names of the page objects change over time
    """

    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.instagram.com/')

    def login(self, username, password):
        """Get the username and password, input in the fields and login"""
        username_input = self.browser.find_element_by_name("username")
        password_input = self.browser.find_element_by_name("password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_link = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button/div")
        login_link.click()
        sleep(5)

    def skip_save_info(self):
        """Skip page asking to save info of login session"""
        try:
            save_info_button = self.browser.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/div/div/div/button")
            save_info_button.click()
        except:
            pass
        sleep(2)

    def skip_notifications(self):
        """Skip page asking to enable notifications"""
        try:
            notificaiton_button = self.browser.find_element_by_xpath(
                "/html/body/div[4]/div/div/div/div[3]/button[2]")
            notificaiton_button.click()
        except:
            pass
        sleep(2)
