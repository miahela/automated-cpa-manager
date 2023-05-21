from functions.google_sheets_manager import GoogleSheetsManager
from functions.web_hosting_manager import WebHostingManager
from functions.web_login_manager import WebLoginManager
from functions.selenium_manager import SeleniumManager
import time


def main():
    url = "https://eu.siteground.com/"

    # File paths
    sheet_credentials_file = "credentials/mp-cpa-managment-49ac92de94ea.json"
    cookies_file = "credentials/my.siteground.com_cookies.json"
    website_credentials_file = "credentials/website_credentials.json"

    # Google Sheets settings
    sheet_name = "Copy of MP CPA Management"
    worksheet_index = 0

    # Initialize managers
    selenium_manager = SeleniumManager()
    web_login_manager = WebLoginManager(selenium_manager)
    web_hosting_manager = WebHostingManager(selenium_manager)
    google_sheets_manager = GoogleSheetsManager(sheet_credentials_file)

    # Get unhosted domains from Google Sheets
    worksheet = google_sheets_manager.get_worksheet(sheet_name, worksheet_index)
    sheet_data = google_sheets_manager.get_worksheet_data(worksheet)
    unhosted_domains = google_sheets_manager.get_unhosted_domains(sheet_data)

    # Login to the website
    web_login_manager.login(url, website_credentials_file, cookies_file)
    time.sleep(8)

    # Add unhosted domains
    for domain in unhosted_domains:
        web_hosting_manager.add_domain(domain)
        print(f"Added {domain} successfully")
        google_sheets_manager.update_domain_on_hosting(worksheet, domain)
        time.sleep(5)

    selenium_manager.quit()


if __name__ == "__main__":
    main()
