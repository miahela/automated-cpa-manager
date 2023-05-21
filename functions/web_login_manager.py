from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from functions.utils import read_json_file


class WebLoginManager:
    xpath_config = {
        "LOGIN_BUTTON_XPATH": '//*[@id="header"]/div/div/div[2]/div/div[4]/a',
        "EMAIL_FIELD_XPATH": '//*[@id="login"]/div/div/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/form/div/label/span[2]/input',
        "NEXT_BUTTON_XPATH": '//*[@id="login"]/div/div/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/form/div/div/button',
        "PASSWORD_FIELD_XPATH": '//*[@id="login"]/div/div/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]/div/form/div/label/span[2]/input',
        "ACCEPT_COOKIES_XPATH": '//*[@id="onetrust-accept-btn-handler"]',
    }

    def __init__(self, selenium_manager):
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
            self.click_element_if_exists(self.xpath_config["ACCEPT_COOKIES_XPATH"])

            self.click_element(self.xpath_config["LOGIN_BUTTON_XPATH"])
            self.fill_field(
                self.xpath_config["EMAIL_FIELD_XPATH"], website_credentials["email"]
            )
            self.click_element(self.xpath_config["NEXT_BUTTON_XPATH"])
            self.fill_field(
                self.xpath_config["PASSWORD_FIELD_XPATH"],
                website_credentials["password"],
            )
            self.click_element(self.xpath_config["NEXT_BUTTON_XPATH"])
            print("Logged in successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def click_element(self, xpath):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()

    def fill_field(self, xpath, data):
        field = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        field.send_keys(data)

    def click_element_if_exists(self, xpath):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            element.click()
        except Exception as e:
            print(f"Element not found. Ignored: {e}")
