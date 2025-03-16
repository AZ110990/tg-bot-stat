from gspread import Client, Spreadsheet, Worksheet, service_account
from oauth2client.service_account import ServiceAccountCredentials

table_link = "https://docs.google.com/spreadsheets/d/1YccG_-Ud2uW1Vsh1jUojvlSWAH9C0i7ZaWLY0QLkQmU"

# def google_auth():
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
#     return gspread.authorize(creds)

def client_init_json() -> Client:
    #Создание клиента для работы с гугл таблицами
    return service_account(filename='collecting-stat-14fda658c3b2.json')

def put_data(date, volume):
    client = client_init_json()
    table = client.open_by_url(table_link)
    worksheet = table.worksheet(title="eggs")
    # Открытие Google Таблицы
    # sheet = client.open("stat").worksheet("eggs")
    data=[date, volume]
    print(data)
    # Запись данных в таблицу
    # sheet.append_row([date, volume])
    worksheet.append_row(data)

# def get_data():
    # client = google_auth()
    # client = client_init_json()
    # table = client.open_by_url(table_link)
    # sheet = client.open("stat").worksheet("average")

def main():
    print("we run google file")
    put_data("11.12.2020", 7)
    print("check sheet")

if __name__ == "__main__":
    main()