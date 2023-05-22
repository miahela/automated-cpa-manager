from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


class SeleniumManager:
    def __init__(self, logger, wait_time=10, headless=False):
        self.logger = logger
        options = Options()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, wait_time)

    def quit(self):
        self.driver.quit()

    def get_driver(self):
        return self.driver

    def click_element(self, xpath):
        self.perform_action_on_element(xpath, "click")

    def double_click_element(self, xpath):
        self.perform_action_on_element(xpath, "double_click")

    def context_click_element(self, xpath):
        self.perform_action_on_element(xpath, "context_click")

    def perform_action_on_element(self, xpath, action_name):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            action = ActionChains(self.driver)
            getattr(action, action_name)(element).perform()
        except Exception as e:
            self.logger.error(f"Error performing {action_name} on element: {e}")

    def accept_cookies(self, xpath='//*[@id="onetrust-accept-btn-handler"]'):
        self.click_element(xpath)

    def fill_field(self, xpath, data):
        try:
            field = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            field.send_keys(data)
            field.send_keys(Keys.ENTER)
        except Exception as e:
            self.logger.error(f"Error filling field: {e}")

    def open_link_new_tab(self, href):
        try:
            initial_tabs = len(self.driver.window_handles)
            self.driver.execute_script("window.open('%s', '_blank')" % href)
            WebDriverWait(self.driver, 10).until(
                lambda driver: len(driver.window_handles) > initial_tabs
            )
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            self.logger.error(f"Error opening link in new tab: {e}")

    def add_cookies(self, cookies, domain="eu.siteground.com"):
        for cookie in cookies:
            try:
                cookie = {
                    k: v for k, v in cookie.items() if k not in ["expiry", "sameSite"]
                }
                cookie["domain"] = domain
                self.driver.add_cookie(cookie)
            except Exception as e:
                self.logger.error(f"Error adding cookie: {e}")
        self.logger.info("Cookies added successfully!")
