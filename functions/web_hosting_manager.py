from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time


class WebHostingManager:
    xpath_config = {
        "WEBSITE_LINK_XPATH": '//*[@id="ua-header"]/div/div/div/nav/ul/li[2]/a',
        "NEW_WEBSITE_BUTTON_XPATH": '//*[@id="sg-ua-main-page"]/div[1]/div/div/div/div[2]/button',
        "EXISTING_DOMAIN_BUTTON_XPATH": '//*[@id="sg-ua-main-page"]/div[2]/div/div/div/div[2]/div/div[2]/button',
        "DOMAIN_FIELD_XPATH": '//*[@id="sg-ua-main-page"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/label/span[2]/input',
        "SKIP_AND_CREATE_BUTTON_XPATH": '//*[@id="sg-ua-main-page"]/div[2]/div/div/div/div[2]/div[2]/span/button/span[1]',
        "FINISH_BUTTON_XPATH": '//*[@id="sg-ua-main-page"]/div[2]/div/div/div/div[2]/div[2]/button',
        "ACCEPT_COOKIES_XPATH": '//*[@id="onetrust-accept-btn-handler"]',
    }

    def __init__(self, selenium_manager):
        self.driver = selenium_manager.driver
        self.wait = selenium_manager.wait

    def add_domain(self, domain):
        try:
            self.click_element(self.xpath_config["ACCEPT_COOKIES_XPATH"])
        except Exception as e:
            print(f"An error occurred: {e}")
        try:
            self.open_link_new_tab("https://my.siteground.com/websites/list")
            self.click_element(self.xpath_config["NEW_WEBSITE_BUTTON_XPATH"])
            self.click_element(self.xpath_config["EXISTING_DOMAIN_BUTTON_XPATH"])
            time.sleep(5)
            self.fill_field(self.xpath_config["DOMAIN_FIELD_XPATH"], domain)
            time.sleep(5)
            self.click_element(self.xpath_config["SKIP_AND_CREATE_BUTTON_XPATH"])
            time.sleep(5)
            self.click_element(self.xpath_config["FINISH_BUTTON_XPATH"])
        except Exception as e:
            print(f"An error occurred: {e}")

    def click_element(self, xpath):
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        element.click()

    def fill_field(self, xpath, data):
        field = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        field.send_keys(data)
        field.send_keys(Keys.ENTER)

    def open_link_new_tab(self, href):
        self.driver.execute_script("window.open('%s', '_blank')" % href)
        self.driver.switch_to.window(self.driver.window_handles[-1])
