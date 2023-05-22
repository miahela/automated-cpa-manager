from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging
import time


class SeleniumManager:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def quit(self):
        self.driver.quit()

    def click_element(self, xpath):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
        except Exception as e:
            logging.error(f"Error clicking element: {e}")

    def double_click_element(self, xpath):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            action = ActionChains(self.driver)
            action.double_click(element)
            action.perform()
        except Exception as e:
            logging.error(f"Error double clicking element: {e}")

    def click_and_verify_with_context_click(self, xpath):
        try:
            time.sleep(1)
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            action = ActionChains(self.driver)
            action.move_to_element(element).context_click().perform()

        except Exception as e:
            logging.error(f"Error clicking element: {e}")

    def accept_cookies(self):
        try:
            element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
                )
            )
            element.click()
        except Exception as e:
            logging.error(f"Error accepting cookies: {e}")

    def fill_field(self, xpath, data):
        try:
            field = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            time.sleep(1)
            field.send_keys(data)
            field.send_keys(Keys.ENTER)
            time.sleep(1)
        except Exception as e:
            logging.error(f"Error filling field: {e}")

    def open_link_new_tab(self, href):
        try:
            self.driver.execute_script("window.open('%s', '_blank')" % href)
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)
        except Exception as e:
            logging.error(f"Error opening link in new tab: {e}")

    def add_cookies(self, cookies):
        for cookie in cookies:
            if "expiry" in cookie:
                cookie.pop("expiry")
            if "sameSite" in cookie:
                cookie.pop("sameSite")
            cookie["domain"] = "eu.siteground.com"
            self.driver.add_cookie(cookie)
        logging.info("Cookies added successfully!")
