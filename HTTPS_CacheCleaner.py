from classes.GoogleSheetsManager import GoogleSheetsManager
from classes.WebHostingManager import WebHostingManager
from classes.SeleniumManager import SeleniumManager
from functions.read_json_file import read_json_file
from functions.setup_logger import setup_logger
import time

logger = setup_logger()
CONFIG = read_json_file("config.json")
true = "TRUE"
false = "FALSE"


class HTTPS_CacheCleaner:
    def __init__(self):
        self.selenium_manager = SeleniumManager(logger)
        self.web_hosting_manager = WebHostingManager(self.selenium_manager, logger)
        self.google_sheets_manager = GoogleSheetsManager(
            CONFIG["sheet_credentials"],
            CONFIG["sheet_name"],
            CONFIG["worksheet_index"],
        )

    def start(self):
        logger.info("*** Starting To Add Domains on Hosting ***")
        self.web_hosting_manager.initialize_session(
            CONFIG["url"], CONFIG["cookies"], CONFIG["local_storage"]
        )
        self.web_hosting_manager.login(CONFIG["website_credentials"])
        self.selenium_manager.click_element("//a[@href='/websites/list']")

    def perform_actions(self):
        unprocessed_domains = self.google_sheets_manager.get_domains_by_condition(
            "Enforce HTTPS", false
        )
        for domain in unprocessed_domains:
            success = self.web_hosting_manager.https_enforce(domain)
            if success is True:
                self.google_sheets_manager.update_domain(domain, "Enforce HTTPS", true)
            success = self.web_hosting_manager.flush_cache(domain)
            if success is True:
                self.google_sheets_manager.update_domain(domain, "Flush Cache", true)


if __name__ == "__main__":
    https_cache_cleaner = HTTPS_CacheCleaner()
    https_cache_cleaner.start()
    https_cache_cleaner.perform_actions()
