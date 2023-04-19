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

all_present = 0
today = date.today()

def main():
    slot_count = 0
    slot_list = []
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

        for row in range(2,76):
            slot_1 = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!C{row}").execute().get("values")[0][0]
           # time.sleep(2)
            slot_2 = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!D{row}").execute().get("values")[0][0]
           # time.sleep(2)
            slot_3 = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!E{row}").execute().get("values")[0][0]
           # time.sleep(2)
            slot_4 = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!F{row}").execute().get("values")[0][0]
           # time.sleep(2)
            slot_5 = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!G{row}").execute().get("values")[0][0]
           # time.sleep(2)
            slot_6 = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!H{row}").execute().get("values")[0][0]
           # time.sleep(2)
            
            slot_list.append(slot_1)
            slot_list.append(slot_2)
            slot_list.append(slot_3)
            slot_list.append(slot_4)
            slot_list.append(slot_5)
            slot_list.append(slot_6)

            slot_count = slot_list.count('TRUE')

            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!I{row}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{slot_count}"]]}).execute()
           # time.sleep(2)
            if(slot_count == 6):
                all_present = True
                sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!J{row}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{all_present}"]]}).execute()
                #time.sleep(2)
            else:
                all_present = False
                sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!J{row}",valueInputOption="USER_ENTERED", body={"values": [[f"{all_present}"]]}).execute()
            slot_count = 0
            slot_list = []
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!K{row}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{today}"]]}).execute()
            #time.sleep(2)
        #result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:C75").execute()

        values = result.get("values", [])
        
    except HttpError as error:
        print(error)
    except TypeError as e:
        print(e)

if __name__ == "__main__":
    main()