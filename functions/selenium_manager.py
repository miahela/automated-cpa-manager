from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


class SeleniumManager:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def quit(self):
        self.driver.quit()
