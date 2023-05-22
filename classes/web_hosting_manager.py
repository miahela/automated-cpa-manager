import time
from selenium.webdriver.common.by import By
from functions.read_json_file import read_json_file
from classes.html_modifier import HTMLModifier


class WebHostingManager:
    def __init__(self, selenium_manager, logger, xpath_config_file="data/xpaths.json"):
        self.selenium_manager = selenium_manager
        self.driver = selenium_manager.get_driver()
        self.wait = selenium_manager.wait
        self.xpath_config = read_json_file(xpath_config_file)
        self.html_modifier = HTMLModifier()
        self.logger = logger

    def login(self, url, website_credentials_file, cookies_file):
        cookies = read_json_file(cookies_file)
        website_credentials = read_json_file(website_credentials_file)

        self.driver.get(url)
        self.selenium_manager.add_cookies(cookies)
        self.driver.refresh()

        try:
            self.selenium_manager.accept_cookies()
            self.fill_login_form(website_credentials)
            self.selenium_manager.open_link_new_tab(
                "https://my.siteground.com/websites/list"
            )
            self.selenium_manager.accept_cookies()
            print("Logged in successfully!")
        except Exception as e:
            self.logger.error(f"Error logging in: {e}")

    def fill_login_form(self, website_credentials):
        self.selenium_manager.click_element(self.xpath_config["LOGIN_BUTTON_XPATH"])
        self.selenium_manager.fill_field(
            self.xpath_config["EMAIL_FIELD_XPATH"], website_credentials["email"]
        )
        self.selenium_manager.click_element(self.xpath_config["NEXT_BUTTON_XPATH"])
        self.selenium_manager.fill_field(
            self.xpath_config["PASSWORD_FIELD_XPATH"], website_credentials["password"]
        )
        self.selenium_manager.click_element(self.xpath_config["NEXT_BUTTON_XPATH"])

    def add_domain(self, domain):
        try:
            self.selenium_manager.click_element(
                self.xpath_config["NEW_WEBSITE_BUTTON_XPATH"]
            )
            self.selenium_manager.click_element(
                self.xpath_config["EXISTING_DOMAIN_BUTTON_XPATH"]
            )
            self.selenium_manager.fill_field(
                self.xpath_config["DOMAIN_FIELD_XPATH"], domain
            )
            self.selenium_manager.click_element(
                self.xpath_config["SKIP_AND_CREATE_BUTTON_XPATH"]
            )
            self.selenium_manager.click_element(
                self.xpath_config["FINISH_BUTTON_XPATH"]
            )
            print(f"Domain {domain} added successfully")
            time.sleep(3)
            handle = self.driver.current_window_handle
            self.selenium_manager.open_link_new_tab(
                "https://my.siteground.com/websites/list"
            )
            return handle
        except Exception as e:
            self.logger.error(f"Error adding domain: {e}")
            return None

    def upload_folder(self, domain_data, window_handle):
        try:
            print(f"Uploading folder for {domain_data['domain_url']}")
            time.sleep(5)
            self.driver.switch_to.window(window_handle)
            time.sleep(5)
            self.selenium_manager.click_element(self.xpath_config["SITE_TOOLS_XPATH"])
            self.temp_upload_file_logic(domain_data)
        except Exception as e:
            self.logger.error(f"Error uploading folder: {e}")

    def only_upload_folder(self, domain_data):
        domain_name = domain_data["domain_url"]
        xpath_expression = (
            f'//div[contains(@class, "sg-container") and .//h2[text()="{domain_name}"]]'
        )
        time.sleep(10)
        container = self.driver.find_element(By.XPATH, xpath_expression)
        button_xpath_expression = (
            './/div[contains(@class, "sg-toolbar")]/div[1]/div/button'
        )
        time.sleep(5)
        button = container.find_element(By.XPATH, button_xpath_expression)
        button.click()
        self.temp_upload_file_logic(domain_data)
        time.sleep(5)
        print("Closing tab...")
        self.driver.back()
        time.sleep(3)
        self.driver.back()

    def temp_upload_file_logic(self, domain_data):
        self.selenium_manager.click_element(self.xpath_config["SITE_SIDE_MENU_XPATH"])
        self.selenium_manager.click_element(self.xpath_config["FILE_MANAGER_XPATH"])
        self.selenium_manager.click_element(
            self.xpath_config["PUBLIC_HTML_EXPAND_XPATH"]
        )
        self.selenium_manager.click_element(self.xpath_config["DEFAULT_HTML_XPATH"])
        self.selenium_manager.click_element(self.xpath_config["DELETE_BUTTON_XPATH"])
        self.selenium_manager.click_element(
            self.xpath_config["CONFIRM_POPUP_BUTTON_XPATH"]
        )
        self.selenium_manager.click_element(self.xpath_config["INDEX_HTML_XPATH"])
        self.selenium_manager.click_element(
            self.xpath_config["CREATE_FILE_BUTTON_XPATH"]
        )
        self.selenium_manager.fill_field(
            self.xpath_config["FILE_NAME_INPUT_XPATH"], "index.html"
        )
        self.selenium_manager.click_element(
            self.xpath_config["CONFIRM_POPUP_BUTTON_XPATH"]
        )
        self.selenium_manager.click_element(self.xpath_config["INDEX_HTML_XPATH"])
        self.selenium_manager.click_element(self.xpath_config["EDIT_BUTTON_XPATH"])
        type = domain_data["type"]
        self.html_modifier.set_file_path(f"data/landing_pages/{type}/index.html")
        new_name = domain_data["full_name"]
        print(f"Changing name to {new_name}")
        new_html = self.html_modifier.change_name(new_name)
        time.sleep(5)
        self.selenium_manager.fill_field(self.xpath_config["TEXT_AREA_XPATH"], new_html)
        self.selenium_manager.click_element(self.xpath_config["SAVE_BUTTON_XPATH"])
