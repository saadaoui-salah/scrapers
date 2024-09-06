import os
import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = './credentials.json'
SPREADSHEET_ID = 'sheet-id'
RANGE_NAME = 'Sheet1!A1:D10'
values = [
    ['Name', 'Age', 'City', 'Occupation'],
    ['Alice', 30, 'New York', 'Engineer'],
    ['Bob', 25, 'Los Angeles', 'Designer'],
    ['Charlie', 35, 'Chicago', 'Manager']
]
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def upload(data):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    body = {
        'values': data
    }
    sheet = service.spreadsheets()
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"{result.get('updatedCells')} cells updated.")