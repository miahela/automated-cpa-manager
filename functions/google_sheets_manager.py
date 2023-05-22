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

    def get_domain_data(self, sheet_data, domain):
        headers = sheet_data[0]
        data = sheet_data[1:]

        domain_name_index = headers.index("Domain")
        domain_purchased_index = headers.index("Domain Purchased")
        domain_hosted_index = headers.index("Domain Added on Hosting")
        upload_folder_index = headers.index("Upload Folder")
        type_index = headers.index("Type")
        full_name_index = headers.index("Full Name")

        for row in data:
            if row[domain_name_index] == domain:
                domain_data = {
                    "domain_url": row[domain_name_index],
                    "domain_purchased": row[domain_purchased_index],
                    "domain_hosted": row[domain_hosted_index],
                    "upload_folder": row[upload_folder_index],
                    "type": row[type_index],
                    "full_name": row[full_name_index],
                }
                return domain_data

        return None

    def get_unhosted_domains(self, sheet_data):
        headers = sheet_data[0]
        data = sheet_data[1:]

        domain_purchased_index = headers.index("Domain Purchased")
        domain_hosted_index = headers.index("Domain Added on Hosting")
        domain_name_index = headers.index("Domain")

        unhosted_domains = []
        for row in data:
            if (
                row[domain_purchased_index] == "TRUE"
                and row[domain_hosted_index] == "FALSE"
            ):
                unhosted_domains.append(row[domain_name_index])

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

    def get_domains_without_folder(self, sheet_data):
        headers = sheet_data[0]
        data = sheet_data[1:]

        domain_hosted_index = headers.index("Domain Added on Hosting")
        upload_folder_index = headers.index("Upload Folder")
        domain_name_index = headers.index("Domain")
        type_index = headers.index("Type")
        full_name_index = headers.index("Full Name")  # Added this line

        domains_without_folder = []
        for row in data:
            if (
                row[domain_hosted_index] == "TRUE"
                and row[upload_folder_index] == "FALSE"
            ):
                # Modified this line
                domains_without_folder.append(row[domain_name_index])

        return domains_without_folder

    def update_domain_with_folder(self, worksheet, domain):
        all_data = self.get_worksheet_data(worksheet)
        domain_index = all_data[0].index("Domain")
        folder_index = all_data[0].index("Upload Folder")

        for i, row in enumerate(all_data):
            if row[domain_index] == domain:
                worksheet.update_cell(i + 1, folder_index + 1, "TRUE")
                print(f"Updated 'Upload Folder' for {domain} to 'TRUE'")
                break
        else:
            print(f"Domain '{domain}' not found in the sheet")
