import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsManager:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.client = self.authenticate_gspread()

    def authenticate_gspread(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(
            self.credentials_file, scopes=scope
        )
        client = gspread.authorize(creds)
        return client

    def get_worksheet(self, sheet_name, worksheet_index):
        sheet = self.client.open(sheet_name)
        worksheet = sheet.get_worksheet(worksheet_index)
        return worksheet

    def get_worksheet_data(self, worksheet):
        list_of_rows = worksheet.get_all_values()
        return list_of_rows

    def get_unhosted_domains(self, sheet_data):
        headers = sheet_data[0]
        data = sheet_data[1:]

        domain_purchased_index = headers.index("Domain Purchased")
        domain_hosted_index = headers.index("Domain Added on Hosting")
        domain_url_index = headers.index("Domain")

        unhosted_domains = []
        for row in data:
            if (
                row[domain_purchased_index] == "TRUE"
                and row[domain_hosted_index] == "FALSE"
            ):
                unhosted_domains.append(row[domain_url_index])

        return unhosted_domains

    def update_domain_on_hosting(self, worksheet, domain):
        all_data = self.get_worksheet_data(worksheet)
        domain_index = all_data[0].index("Domain")
        hosting_index = all_data[0].index("Domain Added on Hosting")

        for i, row in enumerate(all_data):
            if row[domain_index] == domain:
                worksheet.update_cell(i + 1, hosting_index + 1, "TRUE")
                print(f"Updated 'Domain Added on Hosting' for {domain} to 'TRUE'")
                break
        else:
            print(f"Domain '{domain}' not found in the sheet")
