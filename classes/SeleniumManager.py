from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class SeleniumManager:
    def __init__(self, logger, wait_time=20, headless=False):
        self.logger = logger
        options = Options()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, wait_time)

    def quit(self):
        self.driver.quit()
        self.logger.info("Selenium driver closed successfully!")

    def get_driver(self):
        return self.driver

    def click_element(self, xpath):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except Exception as e:
            self.logger.error(f"Error clicking element {xpath}: {e}")

    def accept_cookies(self, xpath='//*[@id="onetrust-accept-btn-handler"]'):
        try:
            cookies = self.driver.find_elements(By.XPATH, xpath)
            if len(cookies) > 0:
                cookies[0].click()
        except Exception as e:
            pass

    def add_local_storage(self, key, value):
        try:
            script = f"localStorage.setItem('{key}', '{value}');"
            self.driver.execute_script(script)
        except Exception as e:
            self.logger.error(f"Error adding local storage: {e}")

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

    def element_exists(self, xpath):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception as e:
            self.logger.error(f"Error checking if element exists: {e}")
            return False

    def wait_until_url_changes(self, url):
        try:
            self.wait.until(EC.url_changes(url))
        except Exception as e:
            self.logger.error(f"Error waiting until url changes: {e}")

    def close_all_tabs_except_first(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
            for handle in self.driver.window_handles[1:]:
                self.driver.switch_to.window(handle)
                self.driver.close()
        except Exception as e:
            self.logger.error(f"Error closing all tabs except first: {e}")

    def open_link(self, href):
        try:
            self.driver.get(href)
        except Exception as e:
            self.logger.error(f"Error opening link: {e}")

    def get_elements(self, xpath):
        try:
            return self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            self.logger.error(f"Error getting elements: {e}")
