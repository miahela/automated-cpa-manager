from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class SeleniumManager:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def click_element(self, xpath):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            element.click()
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Element not found: {xpath}")

    def fill_field(self, xpath, data):
        try:
            field = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            field.send_keys(data)
            field.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Element not found: {xpath}")

    def click_element_if_exists(self, xpath):
        try:
            self.click_element(xpath)
        except Exception as e:
            print(f"Element not found. Ignored: {e}")

    def open_link_new_tab(self, href):
        try:
            self.driver.execute_script("window.open('%s', '_blank')" % href)
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Element not found: {href}")

    def quit(self):
        self.driver.quit()
