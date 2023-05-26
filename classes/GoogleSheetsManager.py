from google.oauth2.service_account import Credentials
import gspread


class GoogleSheetsManager:
    def __init__(self, credentials_file, sheet_name, worksheet_indexes):
        self.credentials_file = credentials_file
        self.client = self.authenticate_gspread()
        worksheet_indexes = worksheet_indexes.split(" ")
        self.worksheets = {
            i: self.get_worksheet(sheet_name, int(i)) for i in worksheet_indexes
        }
        self.domain_worksheet_map = self._create_domain_worksheet_map()

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

    def get_worksheet_data(self, worksheet_index):
        return self.worksheets[worksheet_index].get_all_values()

    def _create_domain_worksheet_map(self):
        domain_map = {}
        for index in self.worksheets:
            data = self.get_worksheet_data(index)
            headers = data[0]
            domain_index = headers.index("Domain")
            for row in data[1:]:
                domain = row[domain_index]
                domain_map[domain] = index
        return domain_map

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
        worksheet_index = self.domain_worksheet_map.get(domain)
        if worksheet_index is not None:
            headers = self.get_worksheet_data(worksheet_index)[0]
            data = self.get_worksheet_data(worksheet_index)[1:]

            for row in data:
                if row[self._get_index(headers, "Domain")] == domain:
                    return self._extract_domain_data(headers, row)
        return None

    def get_domains_by_condition(self, condition_field, condition_value):
        result = []

        for worksheet_index in self.worksheets:
            headers = self.get_worksheet_data(worksheet_index)[0]
            data = self.get_worksheet_data(worksheet_index)[1:]

            for row in data:
                index = self._get_index(headers, condition_field)
                if row[index] == condition_value:
                    result.append(row[self._get_index(headers, "Domain")])

        return result

    def update_domain(self, domain, field_name, new_value):
        worksheet_index = self.domain_worksheet_map.get(domain)
        if worksheet_index is not None:
            all_data = self.get_worksheet_data(worksheet_index)
            domain_index = all_data[0].index("Domain")
            field_index = all_data[0].index(field_name)

            for i, row in enumerate(all_data):
                if row[domain_index] == domain:
                    self.worksheets[worksheet_index].update_cell(
                        i + 1, field_index + 1, new_value
                    )
                    print(
                        f"Updated '{field_name}' for {domain} to '{new_value}' in worksheet index {worksheet_index}"
                    )
                    return
        print(f"Domain '{domain}' not found in the sheet")
