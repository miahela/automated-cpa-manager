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


class ContentUpdater:
    def __init__(self):
        self.selenium_manager = SeleniumManager(logger)
        self.web_hosting_manager = WebHostingManager(self.selenium_manager, logger)
        self.google_sheets_manager = GoogleSheetsManager(
            CONFIG["sheet_credentials"], CONFIG["sheet_name"], CONFIG["worksheet_index"]
        )

    def start(self):
        logger.info("*** Starting To Add Domains on Hosting ***")
        self.web_hosting_manager.initialize_session(
            CONFIG["url"], CONFIG["cookies"], CONFIG["local_storage"]
        )
        self.web_hosting_manager.login(CONFIG["website_credentials"])
        self.selenium_manager.click_element("//a[@href='/websites/list']")

    def delete_old_content(self):
        self.selenium_manager.click_element(
            '//nav[contains(@class,"side-navigation")]//*[contains(text(), "public_html")]'
        )
        time.sleep(2)
        old_content = self.selenium_manager.get_elements(
            '//div[contains(@class,"dropzone")]//div[contains(@class, "content__row content__row--clickabel")]',
        )
        if len(old_content) == 0:
            print("No old content to delete :)")
            return
        print(f"Deleting {len(old_content)} old content")
        for content in old_content:
            time.sleep(2)
            self.web_hosting_manager.delete_element(content)
            time.sleep(2)

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
    content_updater.start()
    content_updater.upload_folders()
