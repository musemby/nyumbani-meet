from django.db.models.signals import post_save
from django.dispatch import receiver
from bookings.models import Booking

from comms.sms import send_bunicom_sms


@receiver(post_save, sender=Booking)
def send_booking_sms(sender, instance, created, **kwargs):
    room = instance.room.name
    start_time = instance.start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = instance.end_time.strftime("%Y-%m-%d %H:%M:%S")
    booked_by = instance.booked_by.name
    phone_number = instance.booked_by.phone_number
    if created:
        message = f"Hello {booked_by}, you have successfully booked {room} from {start_time} to {end_time}."
        send_bunicom_sms(message, [instance.booked_by.phone_number])
