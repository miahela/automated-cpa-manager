from functions.google_sheets_manager import GoogleSheetsManager
from functions.web_hosting_manager import WebHostingManager
from functions.selenium_manager import SeleniumManager
import logging
import time

logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d in %(funcName)s",
)

# File paths
SHEET_CREDENTIALS_FILE = "data/mp-cpa-managment-49ac92de94ea.json"
COOKIES_FILE = "data/my.siteground.com_cookies.json"
WEBSITE_CREDENTIALS_FILE = "data/website_credentials.json"

# Settings
SHEET_NAME = "Copy of MP CPA Management"
WORKSHEET_INDEX = 1
URL = "https://eu.siteground.com/"


def add_domains(
    unhosted_domains, web_hosting_manager, google_sheets_manager, worksheet
):
    newly_hosted_domains = []
    for domain in unhosted_domains:
        handle = web_hosting_manager.add_domain(domain)
        if handle is None:
            logging.error(f"Failed to add {domain} :(")
            print(f"Failed to add {domain} :(")
            continue
        google_sheets_manager.update_domain_on_hosting(worksheet, domain)
        newly_hosted_domains.append({"handle": handle, "domain": domain})
    return newly_hosted_domains


def upload_domains(
    newly_hosted_domains,
    web_hosting_manager,
    google_sheets_manager,
    sheet_data,
    worksheet,
):
    for domain_info in newly_hosted_domains:
        window_handle = domain_info["handle"]
        domain = domain_info["domain"]
        domain_data = google_sheets_manager.get_domain_data(sheet_data, domain)
        successful_hosting_flag = web_hosting_manager.upload_folder(
            domain_data, window_handle
        )
        if not successful_hosting_flag:
            logging.error(f"Error uploading {domain}")
            print(f"Error uploading {domain}")
            continue
        google_sheets_manager.update_domain_with_folder(worksheet, domain)


def main():
    selenium_manager = SeleniumManager()
    web_hosting_manager = WebHostingManager(selenium_manager)
    google_sheets_manager = GoogleSheetsManager(SHEET_CREDENTIALS_FILE)

    worksheet = google_sheets_manager.get_worksheet(SHEET_NAME, WORKSHEET_INDEX)
    sheet_data = google_sheets_manager.get_worksheet_data(worksheet)
    unhosted_domains = google_sheets_manager.get_unhosted_domains(sheet_data)

    web_hosting_manager.login(URL, WEBSITE_CREDENTIALS_FILE, COOKIES_FILE)

    # newly_hosted_domains = add_domains(
    #     unhosted_domains, web_hosting_manager, google_sheets_manager, worksheet
    # )

    # upload_domains(
    #     newly_hosted_domains,
    #     web_hosting_manager,
    #     google_sheets_manager,
    #     sheet_data,
    #     worksheet,
    # )

    get_domains_without_folder = google_sheets_manager.get_domains_without_folder(
        sheet_data
    )

    for domain in get_domains_without_folder:
        domain_data = google_sheets_manager.get_domain_data(sheet_data, domain)
        web_hosting_manager.only_upload_folder(domain_data)
        google_sheets_manager.update_domain_with_folder(worksheet, domain)

    print("All folders uploaded successfully! :)")

    print("Quitting the browser...")
    time.sleep(3)

    selenium_manager.quit()


if __name__ == "__main__":
    main()
