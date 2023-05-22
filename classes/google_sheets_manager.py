import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsManager:
    def __init__(self, credentials_file, sheet_name, worksheet_index):
        self.credentials_file = credentials_file
        self.client = self.authenticate_gspread()
        self.worksheet = self.get_worksheet(sheet_name, worksheet_index)

    def authenticate_gspread(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(
            self.credentials_file, scopes=scope
        )
        return gspread.authorize(creds)

    def get_worksheet(self, sheet_name, worksheet_index):
        sheet = self.client.open(sheet_name)
        return sheet.get_worksheet(worksheet_index)

    @property
    def worksheet_data(self):
        return self.worksheet.get_all_values()

    @staticmethod
    def _get_index(headers, field_name):
        return headers.index(field_name)

    @staticmethod
    def _extract_domain_data(headers, row):
        return {
            header: row[GoogleSheetsManager._get_index(headers, header)]
            for header in headers
        }

    def get_domain_data(self, domain):
        headers = self.worksheet_data[0]
        data = self.worksheet_data[1:]

        for row in data:
            if row[self._get_index(headers, "Domain")] == domain:
                return self._extract_domain_data(headers, row)

        return None

    def get_domains_by_condition(self, condition_field, condition_value):
        headers = self.worksheet_data[0]
        data = self.worksheet_data[1:]

        return [
            row[self._get_index(headers, "Domain")]
            for row in data
            if row[self._get_index(headers, condition_field)] == condition_value
        ]

    def update_domain(self, domain, field_name, new_value):
        all_data = self.worksheet_data
        domain_index = all_data[0].index("Domain")
        field_index = all_data[0].index(field_name)

        for i, row in enumerate(all_data):
            if row[domain_index] == domain:
                self.worksheet.update_cell(i + 1, field_index + 1, new_value)
                print(f"Updated '{field_name}' for {domain} to '{new_value}'")
                return
        print(f"Domain '{domain}' not found in the sheet")
