import gspread
from oauth2client.service_account import ServiceAccountCredentials

def google_auth():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
    client = gspread.authorize(creds)

def put_data(client, date, volume):
    # Открытие Google Таблицы
    sheet = client.open("stat").worksheet("eggs")

    # Запись данных в таблицу
    sheet.append_row([date, volume])

def get_data(client):
    sheet = client.open("stat").worksheet("average")
