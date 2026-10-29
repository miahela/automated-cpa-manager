"""Read the configured worksheet and open the dashboard without changing either."""
from classes.GoogleSheetsManager import GoogleSheetsManager
from classes.SeleniumManager import SeleniumManager
from functions.load_config import load_config
from functions.setup_logger import setup_logger


def main():
    config = load_config()
    sheets = GoogleSheetsManager(config['sheet_credentials'], config['sheet_name'],
                                 config['worksheet_index'])
    for column in ('Domain Added on Hosting', 'Upload Folder', 'Name Changed',
                   'Enforce HTTPS', 'Flush Cache'):
        pending = sheets.get_domains_by_condition(column, 'FALSE')
        print(f'{column}: {len(pending)} pending')
    browser = SeleniumManager(setup_logger())
    try:
        browser.open_link(config['websites_url'])
        input('Dashboard opened. Press Enter to close Chrome: ')
    finally:
        browser.quit()


if __name__ == '__main__':
    main()
