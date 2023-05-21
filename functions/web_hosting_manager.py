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
        self.selenium_manager = selenium_manager
        self.driver = selenium_manager.driver
        self.wait = selenium_manager.wait

    def add_domain(self, domain):
        self.selenium_manager.click_element_if_exists(
            self.xpath_config["ACCEPT_COOKIES_XPATH"]
        )
        try:
            self.selenium_manager.open_link_new_tab(
                "https://my.siteground.com/websites/list"
            )
            time.sleep(5)
            self.selenium_manager.click_element(
                self.xpath_config["NEW_WEBSITE_BUTTON_XPATH"]
            )
            time.sleep(5)
            self.selenium_manager.click_element(
                self.xpath_config["EXISTING_DOMAIN_BUTTON_XPATH"]
            )
            time.sleep(5)
            self.selenium_manager.fill_field(
                self.xpath_config["DOMAIN_FIELD_XPATH"], domain
            )
            time.sleep(5)
            self.driselenium_managerver.click_element(
                self.xpath_config["SKIP_AND_CREATE_BUTTON_XPATH"]
            )
            time.sleep(5)
            self.selenium_manager.click_element(
                self.xpath_config["FINISH_BUTTON_XPATH"]
            )
        except Exception as e:
            print(f"An error occurred: {e}")
