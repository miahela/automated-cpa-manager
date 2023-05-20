import gspread
from google.oauth2.service_account import Credentials

def connect_to_sheet(credentials_file, sheet_name, worksheet_index):

    # Define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Add your Service Account file
    creds = Credentials.from_service_account_file(credentials_file, scopes=scope)

    client = gspread.authorize(creds)

    # Open the Google Spreadsheet by its name (make sure you have shared it with the client_email from JSON file)
    sheet = client.open(sheet_name)

    # Select a worksheet from the Spreadsheet
    worksheet = sheet.get_worksheet(worksheet_index)

    # Get all values from the worksheet
    list_of_rows = worksheet.get_all_values()

    # Print all rows
    for row in list_of_rows:
        print(row)
