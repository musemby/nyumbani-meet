import requests

from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, sender=None, recipients=[]):
    sender = sender or settings.DEFAULT_SENDER_EMAIL
    send_mail(subject, message, sender, recipients)


def send_org_join_request_email():
    print('Sent join request email')


def send_org_join_request_approved_email():
    print('Sent join request approved email')


def send_org_join_request_rejected_email():
    print('Sent join request rejected email')


def send_added_to_org_email(member):
    full_name = member.user.full_name
    email = member.user.email
    subject = "Activate your SASDEF HR Account"
    message = f"""
    Hello {full_name},

    You have been added to the SASDEF HR portal with the email {email}.
    A seperate email will be sent to you to allow you to reset your password and access the portal.
    """

    send_email(subject, message, recipients=[email])
    
    reset_url = f'{settings.API_DOMAIN}/authorization/users/reset_password/'
    data = {
        'email': email
    }
    requests.post(reset_url, data)
