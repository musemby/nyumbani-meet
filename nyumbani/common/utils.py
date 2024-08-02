import csv
import datetime

from phonenumbers import parse, format_number, PhoneNumberFormat, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError


def parse_and_format_phone_number(phone_number):
    regions_to_try = ['KE', None]
    
    for region in regions_to_try:
        try:
            parsed_number = parse(phone_number, region)
            
            if is_valid_number(parsed_number):
                # Format the number in E.164 format (with '+' prefix)
                e164_format = format_number(parsed_number, PhoneNumberFormat.E164)
                
                # Remove the '+' sign from the beginning
                return e164_format
        except NumberParseException:
            continue

    raise ValidationError("Invalid phone number")


def is_weekend(date):
    return True if date.weekday() > 4 else False


def is_weekday(date):
    return True if date.weekday() < 5 else False


def create_csv(file_path, header_row, data_rows):
    with open(file_path, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header_row)
        for data_row in data_rows:
            writer.writerow(data_row)


def normalize_phone_number(number):
    return number
