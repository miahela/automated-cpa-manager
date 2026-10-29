from classes.GoogleSheetsManager import GoogleSheetsManager
from classes.WebHostingManager import WebHostingManager
from classes.SeleniumManager import SeleniumManager
from functions.load_config import load_config
from functions.setup_logger import setup_logger
import time

logger = setup_logger()

true = "TRUE"
false = "FALSE"


class ContentUpdater:
    def __init__(self):
        self.config = load_config()
        self.selenium_manager = SeleniumManager(logger)
        self.web_hosting_manager = WebHostingManager(
            self.selenium_manager, logger, self.config["xpath_config"],
            self.config["landing_pages"], self.config["websites_url"]
        )
        self.google_sheets_manager = GoogleSheetsManager(
            self.config["sheet_credentials"], self.config["sheet_name"], self.config["worksheet_index"]
        )

    def start(self):
        logger.info("*** Starting To Add Domains on Hosting ***")
        self.web_hosting_manager.initialize_session(
            self.config["url"], self.config["cookies"], self.config["local_storage"]
        )
        self.web_hosting_manager.login(self.config["website_credentials"])
        self.selenium_manager.click_element("//a[@href='/websites/list']")

    def delete_old_content(self):
        self.web_hosting_manager.delete_old_files()

    def upload_folders(self):
        domains_without_folder = self.google_sheets_manager.get_domains_by_condition(
            "Upload Folder", false
        )
        if len(domains_without_folder) == 0:
            print("No domains to upload folder :)")
            return

        for domain in domains_without_folder:
            self.web_hosting_manager.navigate_to_file_manager(domain)
            self.delete_old_content()
            domain_info = self.google_sheets_manager.get_domain_data(domain)
            succesful_upload = self.web_hosting_manager.upload_new_file(domain_info)
            if succesful_upload is False:
                logger.error(f"Failed to upload folder for {domain} :(")
                print(f"Failed to upload folder for {domain} :(")
                continue
            self.google_sheets_manager.update_domain(domain, "Upload Folder", "TRUE")
            self.google_sheets_manager.update_domain(domain, "Name Changed", "TRUE")

        logger.info("*** Finished Uploading Folders ***")


if __name__ == "__main__":
    content_updater = ContentUpdater()
    try:
        content_updater.start()
        content_updater.upload_folders()
    finally:
        content_updater.selenium_manager.quit()
