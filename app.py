from classes.google_sheets_manager import GoogleSheetsManager
from classes.web_hosting_manager import WebHostingManager
from classes.selenium_manager import SeleniumManager
from functions.setup_logger import setup_logger

logger = setup_logger()

# File paths and settings
CONFIG = {
    "sheet_credentials": "data/mp-cpa-managment-49ac92de94ea.json",
    "cookies": "data/my.siteground.com_cookies.json",
    "website_credentials": "data/website_credentials.json",
    "sheet_name": "Copy of MP CPA Management",
    "worksheet_index": 1,
    "url": "https://eu.siteground.com/",
}


class App:
    def __init__(self):
        self.selenium_manager = SeleniumManager(logger)
        self.web_hosting_manager = WebHostingManager(self.selenium_manager, logger)
        self.google_sheets_manager = GoogleSheetsManager(
            CONFIG["sheet_credentials"], CONFIG["sheet_name"], CONFIG["worksheet_index"]
        )

    def add_domains(self, unhosted_domains):
        newly_hosted_domains = []
        for domain in unhosted_domains:
            handle = self.web_hosting_manager.add_domain(domain)
            if handle is None:
                logger.error(f"Failed to add {domain} :(")
                print(f"Failed to add {domain} :(")
                continue
            self.google_sheets_manager.update_domain(
                domain, "Domain Added on Hosting", "True"
            )
            newly_hosted_domains.append({"handle": handle, "domain": domain})
        return newly_hosted_domains

    def upload_files_to_domains(self, newly_hosted_domains):
        for domain_info in newly_hosted_domains:
            window_handle = domain_info["handle"]
            domain = domain_info["domain"]
            domain_data = self.google_sheets_manager.get_domain_data(domain)
            successful_hosting_flag = self.web_hosting_manager.upload_folder(
                domain_data, window_handle
            )
            if not successful_hosting_flag:
                logger.error(f"Error uploading {domain}")
                print(f"Error uploading {domain}")
                continue
            self.google_sheets_manager.update_domain(domain, "Upload Folder", "True")

    def main(self):
        logger.info("******* Starting *******")
        unhosted_domains = self.google_sheets_manager.get_domains_by_condition(
            "Domain Added on Hosting", "False"
        )

        self.web_hosting_manager.login(
            CONFIG["url"], CONFIG["website_credentials"], CONFIG["cookies"]
        )

        newly_hosted_domains = self.add_domains(unhosted_domains)
        self.upload_files_to_domains(newly_hosted_domains)

        domains_without_folder = self.google_sheets_manager.get_domains_by_condition(
            "Upload Folder", "False"
        )
        for domain in domains_without_folder:
            domain_data = self.google_sheets_manager.get_domain_data(domain)
            self.web_hosting_manager.only_upload_folder(domain_data)
            self.google_sheets_manager.update_domain(domain, "Upload Folder", "True")

        print("Done :)")
        logger.info("******* Done *******")


if __name__ == "__main__":
    app = App()
    app.main()
    app.selenium_manager.quit()
