from functions.utils import read_json_file
import time


class WebLoginManager:
    xpath_config = {
        "LOGIN_BUTTON_XPATH": '//*[@id="header"]/div/div/div[2]/div/div[4]/a',
        "EMAIL_FIELD_XPATH": '//*[@id="login"]/div/div/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/form/div/label/span[2]/input',
        "NEXT_BUTTON_XPATH": '//*[@id="login"]/div/div/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/form/div/div/button',
        "PASSWORD_FIELD_XPATH": '//*[@id="login"]/div/div/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]/div/form/div/label/span[2]/input',
        "ACCEPT_COOKIES_XPATH": '//*[@id="onetrust-accept-btn-handler"]',
    }

    def __init__(self, selenium_manager):
        self.selenium_manager = selenium_manager
        self.driver = selenium_manager.driver
        self.wait = selenium_manager.wait

    def add_cookies(self, cookies):
        for cookie in cookies:
            if "expiry" in cookie:
                cookie.pop("expiry")
            if "sameSite" in cookie:
                cookie.pop("sameSite")
            cookie["domain"] = "eu.siteground.com"
            self.driver.add_cookie(cookie)

    def login(self, url, website_credentials_file, cookies_file):
        cookies = read_json_file(cookies_file)
        website_credentials = read_json_file(website_credentials_file)

        self.driver.get(url)
        self.add_cookies(cookies)

        self.driver.refresh()

        try:
            self.selenium_manager.click_element_if_exists(
                self.xpath_config["ACCEPT_COOKIES_XPATH"]
            )
            time.sleep(5)
            self.selenium_manager.click_element(self.xpath_config["LOGIN_BUTTON_XPATH"])
            time.sleep(5)
            self.selenium_manager.fill_field(
                self.xpath_config["EMAIL_FIELD_XPATH"], website_credentials["email"]
            )
            time.sleep(5)
            self.selenium_manager.click_element(self.xpath_config["NEXT_BUTTON_XPATH"])
            time.sleep(5)
            self.selenium_manager.fill_field(
                self.xpath_config["PASSWORD_FIELD_XPATH"],
                website_credentials["password"],
            )
            time.sleep(5)
            self.selenium_manager.click_element(self.xpath_config["NEXT_BUTTON_XPATH"])
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
