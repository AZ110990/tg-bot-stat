import os
from gspread import Client, Spreadsheet, Worksheet, service_account
from gspread.exceptions import APIError
from datetime import date
from io import StringIO
from calendar import month_name
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

from dotenv import load_dotenv
load_dotenv()
table_id = os.getenv("TABLE_STAT_ID")

# table_id = os.environ.get("TABLE_STAT_LINK")


def client_init_json() -> Client:
    #Создание клиента для работы с гугл таблицами
    return service_account(filename='collecting-stat-14fda658c3b2.json')

def open_sheet(title):
    client = client_init_json()
    table = client.open_by_key(table_id)
    return table.worksheet(title=title)

def put_data(volume):
    date_to_save = date.today().strftime("%m.%d.%Y")
    data_to_save = [date_to_save, volume]
    worksheet = open_sheet("eggs")
    try:
        worksheet.append_row(data_to_save)
        return (f"Данные успешно сохранены.")
    except APIError as e:
        return (f"Произошла ошибка при сохранении данных: {e}\nОбратитесь к разработчику")
    except Exception as e:
        return (f"Произошла неизвестная ошибка при сохранении данных: {e}\nОбратитесь к разработчику")

def get_data():
    worksheet = open_sheet("averages")
    gsheet_data = worksheet.get_all_values()[1:]
    result = {}
    for row in gsheet_data:
        year, month, total, average = row
        if year not in result:
            result[year] = {}
        result[year][month] = {
            "total": int(total),
            "average": float(average.replace(",", "."))
        }
    output = StringIO()

    for year, months in result.items():
        output.write(f"Год {year}\n")
        for month, data in months.items():
            output.write(f"   {month_name[int(month)]} - Всего {data['total']} ({data['average']} в среднем)\n")

    return output.getvalue()