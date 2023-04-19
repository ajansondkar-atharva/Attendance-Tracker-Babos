import os
from datetime import date
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1-nNtq-MYzNzyGOdXnUivam7BSvlpbzTCLsLx-1K09fs"

today = date.today()
def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json",SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        total_students = [x for x in range(1,77)]
        print(total_students)
        with open('messages.txt', 'r') as f:
            absent_students=f.read()
        
        int_absent_students = list(map(int, absent_students.split()))
        present_students = list(set(total_students) - set(int_absent_students))

        for i in total_students:
                time.sleep(1)
                if i in present_students:
                    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!C{i+1}",
                                valueInputOption="USER_ENTERED", body={"values": [[f"{True}"]]}).execute()
                    print(f"Checking for {i}")

    except HttpError as error:
        print(error)
    except TypeError as e:
        print(e)

if __name__ == "__main__":
    main()