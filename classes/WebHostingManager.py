from functions.read_json_file import read_json_file
from classes.DiskFileManager import DiskFileManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import os


class WebHostingManager:
    def __init__(self, selenium_manager, logger, xpath_config_file="data/xpaths.json"):
        self.selenium_manager = selenium_manager
        self.driver = selenium_manager.get_driver()
        self.wait = selenium_manager.wait
        self.xpath_config = read_json_file(xpath_config_file)
        self.disk_file_manager = DiskFileManager()
        self.logger = logger

    def initialize_session(self, url, cookies_file, local_storage={}):
        cookies = read_json_file(cookies_file)
        local_storage = read_json_file(local_storage)
        self.driver.get(url)
        self.selenium_manager.add_cookies(cookies)
        for key, value in local_storage.items():
            self.selenium_manager.add_local_storage(key, value)
        self.driver.refresh()

    def login(self, website_credentials_file):
        website_credentials = read_json_file(website_credentials_file)
        self.selenium_manager.accept_cookies()

        try:
            self.selenium_manager.click_element(self.xpath_config["LOGIN_BUTTON_XPATH"])
            self.selenium_manager.fill_field(
                self.xpath_config["EMAIL_FIELD_XPATH"], website_credentials["email"]
            )
            self.selenium_manager.fill_field(
                self.xpath_config["PASSWORD_FIELD_XPATH"],
                website_credentials["password"],
            )

            current_url = self.driver.current_url
            self.selenium_manager.wait_until_url_changes(current_url)
            self.selenium_manager.accept_cookies()
            print("Logged in successfully!")
        except Exception as e:
            self.logger.error(f"Error logging in: {e}")
            sys.exit(1)

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
            self.logger.info(f"Domain {domain} added successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error adding domain: {e}")
            return False

    def delete_element(self, element_xpath, name="old content"):
        if self.selenium_manager.element_exists(element_xpath):
            self.selenium_manager.click_element(element_xpath)
            self.selenium_manager.click_element(
                self.xpath_config["DELETE_BUTTON_XPATH"]
            )
            time.sleep(3)
            self.selenium_manager.click_element(
                self.xpath_config["CONFIRM_POPUP_BUTTON_XPATH"]
            )
            self.logger.info(f"Element {name} deleted successfully")
        else:
            self.logger.info(f"Element {name} not found")

    def delete_file(self, filename="Default.html"):
        file_xpath = (
            f'//div[contains(@class,"dropzone")]//*[contains(text(), "{filename}")]'
        )
        self.delete_element(file_xpath, filename)

    def delete_old_files(self):
        self.selenium_manager.click_element(
            self.xpath_config["PUBLIC_HTML_EXPAND_XPATH"]
        )
        time.sleep(2)
        first_element_xpath = '//*[@id="root"]/div/div/div[2]/main/div/div[2]/div/div/article/section/div/div/div/table/tbody/tr[1]/td[1]/div'
        while self.selenium_manager.element_exists(first_element_xpath):
            self.delete_element(first_element_xpath)

    def unzip_inside_website(self, domain_name):
        self.selenium_manager.click_element(
            f'//nav[contains(@class,"side-navigation")]//*[contains(text(), "{domain_name}")]'
        )

        self.selenium_manager.click_element(
            f'//div[contains(@class,"dropzone")]//*[contains(text(), "public_html.zip")]',
        )

        self.selenium_manager.click_element(
            '//*[@id="root"]/div/div/div[2]/main/div/div[2]/div/div/div[1]/div[2]/div/span[13]/span[1]'
        )
        self.selenium_manager.click_element(
            f'//nav[contains(@class,"side-navigation")]//*[contains(text(), "{domain_name}")]'
        )
        self.delete_file("public_html.zip")

    def navigate_to_file_manager(self, domain):
        self.selenium_manager.open_link("https://my.siteground.com/websites/list")
        self.selenium_manager.click_element(
            f'//*[contains(text(), "{domain}")]/ancestor::div[contains(@class, "sg-container")]//*[contains(text(), "Site Tools")]'
        )
        self.selenium_manager.click_element(self.xpath_config["SITE_SIDE_MENU_XPATH"])
        self.selenium_manager.click_element(self.xpath_config["FILE_MANAGER_XPATH"])

    def upload_new_file(self, domain_info):
        type = domain_info["Type"]

        self.selenium_manager.click_element(
            f'//nav[contains(@class,"side-navigation")]//*[contains(text(), "{domain_info["Domain"]}")]'
        )

        self.selenium_manager.click_element(
            '//*[@id="root"]/div/div/div[2]/main/div/div[2]/div/div/div[1]/div[2]/div/span[3]/span[1]'
        )

        root_folder_path = os.path.join(os.getcwd(), "data", "landing_pages", type)
        zip_path = os.path.join(os.getcwd(), "data", "landing_pages", "public_html.zip")

        self.disk_file_manager.change_html_content(
            root_folder_path, domain_info["Full Name"]
        )

        self.disk_file_manager.zip_folder_contents(root_folder_path, zip_path)

        try:
            self.driver.find_elements(By.ID, "fm-upload")[0].send_keys(zip_path)
        except Exception as e:
            self.logger.error(f"Error uploading file: {e}")
            return False

        time.sleep(10)

        self.unzip_inside_website(domain_info["Domain"])

    def https_enforce(self, domain):
        try:
            self.selenium_manager.open_link("https://my.siteground.com/websites/list")
            self.selenium_manager.click_element(
                f'//*[contains(text(), "{domain}")]/ancestor::div[contains(@class, "sg-container")]//*[contains(text(), "Site Tools")]'
            )
            self.selenium_manager.click_element(
                self.xpath_config["security_side_menu_xpath"]
            )
            self.selenium_manager.click_element(
                self.xpath_config["https_enforce_side_xpath"]
            )
            if self.selenium_manager.element_exists(self.xpath_config["get_ssl_xpath"]):
                return False
            self.selenium_manager.click_element(self.xpath_config["switch_xpath"])
            return True
        except Exception as e:
            self.logging.error(f"Error enabling https for {domain}: {e}")
            return False

    def flush_cache(self, domain):
        try:
            self.selenium_manager.click_element(
                self.xpath_config["speed_side_menu_xpath"]
            )
            self.selenium_manager.click_element(self.xpath_config["caching_side_xpath"])
            self.selenium_manager.click_element(
                self.xpath_config["dynamic_cache_xpath"]
            )
            self.selenium_manager.click_element(self.xpath_config["flush_action_xpath"])
            return True
        except Exception as e:
            self.logging.error(f"Error flushing cache for {domain}: {e}")
            return False
