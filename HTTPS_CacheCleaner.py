from classes.GoogleSheetsManager import GoogleSheetsManager
from classes.WebHostingManager import WebHostingManager
from classes.SeleniumManager import SeleniumManager
from functions.load_config import load_config
from functions.setup_logger import setup_logger
import time

logger = setup_logger()

true = "TRUE"
false = "FALSE"


class HTTPS_CacheCleaner:
    def __init__(self):
        self.config = load_config()
        self.selenium_manager = SeleniumManager(logger)
        self.web_hosting_manager = WebHostingManager(
            self.selenium_manager, logger, self.config["xpath_config"],
            self.config["landing_pages"], self.config["websites_url"]
        )
        self.google_sheets_manager = GoogleSheetsManager(
            self.config["sheet_credentials"],
            self.config["sheet_name"],
            self.config["worksheet_index"],
        )

    def start(self):
        logger.info("*** Starting HTTPS Enforcement and Cache Flush ***")
        self.web_hosting_manager.initialize_session(
            self.config["url"], self.config["cookies"], self.config["local_storage"]
        )
        self.web_hosting_manager.login(self.config["website_credentials"])
        self.selenium_manager.click_element("//a[@href='/websites/list']")

    def perform_actions(self):
        unprocessed_domains = self.google_sheets_manager.get_domains_by_condition(
            "Enforce HTTPS", false
        )
        for domain in unprocessed_domains:
            success = self.web_hosting_manager.https_enforce(domain)
            if success is True:
                self.google_sheets_manager.update_domain(domain, "Enforce HTTPS", true)
        for domain in self.google_sheets_manager.get_domains_by_condition("Flush Cache", false):
            success = self.web_hosting_manager.flush_cache(domain)
            if success is True:
                self.google_sheets_manager.update_domain(domain, "Flush Cache", true)


if __name__ == "__main__":
    https_cache_cleaner = HTTPS_CacheCleaner()
    try:
        https_cache_cleaner.start()
        https_cache_cleaner.perform_actions()
    finally:
        https_cache_cleaner.selenium_manager.quit()
