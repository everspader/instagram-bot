from time import sleep
from selenium import webdriver

from login_page import LoginPage
import bot_engine


# with open('settings.json', 'r') as f:
#     data = f.read()
# obj = json.loads(data)
# username = obj['instagram']['username']
# password = obj['instagram']['password']

# def test_login_page(browser):
#     login_page = LoginPage(browser)
#     login_page.login(username, password)

#     errors = browser.find_elements_by_css_selector('#error_message')
#     assert len(errors) == 0

# webdriver = webdriver.Firefox()
webdriver = webdriver.Chrome()
webdriver.implicitly_wait(5)

bot_engine.init(webdriver)
bot_engine.update(webdriver)

# browser.close()
