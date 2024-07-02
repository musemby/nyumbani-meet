import csv
import datetime

from openpyxl import Workbook


def is_weekend(date):
    return True if date.weekday() > 4 else False


def is_weekday(date):
    return True if date.weekday() < 5 else False


def convert_csv_to_xlsx(file_path):
    wb = Workbook()
    ws = wb.active
    with open(file_path, 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    name = file_path.split('.')[0]
    xlsx_path = f'{name}.xlsx'
    wb.save(f'{xlsx_path}')
    return xlsx_path


def create_csv(file_path, header_row, data_rows):
    with open(file_path, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header_row)
        for data_row in data_rows:
            writer.writerow(data_row)


def normalize_phone_number(number):
    return number
