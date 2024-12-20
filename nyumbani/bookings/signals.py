from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from bookings.models import Booking
from organizations.models import UserOrganization

from comms.sms import send_bunicom_sms, send_sms_to_console


@receiver(post_save, sender=Booking)
def send_booking_sms(sender, instance, created, **kwargs):
    room = instance.room.name
    start_time = instance.start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = instance.end_time.strftime("%Y-%m-%d %H:%M:%S")
    booked_by = instance.booked_by.name
    phone_number = instance.booked_by.phone_number
    
    # admin message
    organization = instance.organization
    admin_phone_numbers = UserOrganization.objects.filter(organization=organization, is_admin=True).values_list(
        'user__phone_number', flat=True
    )
    admin_phone_numbers = list(admin_phone_numbers)
    admin_message = f"Hello. There is a new booking by {booked_by} for {room} from {start_time} to {end_time}."
    

    if created:
        message = f"Hello {booked_by}, you have successfully booked {room} from {start_time} to {end_time}."
        if settings.ENVIRONMENT == "PRODUCTION":
            send_bunicom_sms(message, [phone_number])
            send_bunicom_sms(admin_message, admin_phone_numbers)

            return

        send_sms_to_console(message, [phone_number])
        send_bunicom_sms(admin_message, admin_phone_numbers)
