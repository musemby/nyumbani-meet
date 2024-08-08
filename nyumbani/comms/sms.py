from json import JSONDecodeError
import logging
import requests

from django.conf import settings
from common.utils import parse_and_format_phone_number

LOGGER = logging.getLogger('__name__')


def send_sms_to_console(message, recipients):
    print('SMS - sent')
    print('From: {}\nTo: {}\n')
    print(message)


def send_bunicom_sms(message, recipients, time_to_send=None):
    for recipient in recipients:
        parsed_recipient = recipient.as_e164
        data = {
            "apikey": settings.BUNICOM_API_KEY,
            "partnerID": settings.BUNICOM_PARTNER_ID,
            "message": message,
            "shortcode": settings.BUNICOM_SHORTCODE,
            "mobile": parsed_recipient,
        }
        if time_to_send:
            data['timeToSend'] = time_to_send # Unix timestamp

        response = requests.post(settings.BUNICOM_SMS_URL, data=data)
        try:
            print(response.json())
        except JSONDecodeError:
            return print(response)


def send_bunicom_bulk_sms(headers, data_records, message_pattern):
    data = {
        "headers": headers,
        "data_records": data_records,
        "message_pattern": message_pattern,
        "apikey": settings.BUNICOM_API_KEY,
        "shortcode": settings.BUNICOM_SHORTCODE,
    }

    response = requests.post(settings.BUNICOM_BULK_SMS_URL, data=data)
    if response.status == 200:
        pass
        # log message ID (json fields?)
    try:
        return response.json()
    except JSONDecodeError:
        return response


def get_bunicom_sms_delivery_report(message_id):
    data = {
        "messageId": settings.BUNICOM_SMS_DELIVERY_REPORT_URL,
        "apikey": settings.BUNICOM_API_KEY,
    }
    response = requests.post(settings.BUNICOM_SMS_DELIVERY_REPORT_URL, data=data)
    try:
        return response.json()
    except JSONDecodeError:
        return response
