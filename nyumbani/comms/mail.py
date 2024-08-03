import requests
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings


def send_zeptomail_email():
    payload = """{
        "from": { 
            "address": "admin@nyumbani.co.ke",
            "name": "Nyumbani Admin"
        },
        "to": [
            {
                "email_address": {
                "address": "musembinzioki@gmail.com",
                "name": "Joseph Musembi"
                }
            }
        ],
        "subject":"Test Email Zepto",
        "htmlbody":"<p>Test email sent successfully.</p>"
    }"""

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': settings.ZEPTO_MAIL_AUTH_KEY,
    }

    response = requests.post(
        settings.ZEPTO_MAIL_URL,
        data=payload,
        headers=headers
    )

    print(response.text)


def send_ventisei_email(subject, body, html_message=None, sender=settings.DEFAULT_SENDER_EMAIL, recipients=[]):

    send_mail(subject, body, sender, recipients, html_message=html_message)

