from bookings.models import Booking
from common.mailer import send_email
from organizations.models import UserOrganization


def send_booking_created_email(booking_id: str):
    print("Sending booking created email")
    # send to booking user
    booking = Booking.objects.get(pk=booking_id)
    user_email = booking.booked_by.email

    subject = "Booking Created"
    message = f"""
    Booking created

    ---
    Description: {booking.description if booking.description is not None else '_'}

    Start Time: {booking.start_time.strftime('%Y-%m-%d %H:%M')}
    End Time: {booking.end_time.strftime('%Y-%m-%d %H:%M')}

    Room: {booking.room.name if booking.room and booking.room.name is not None else '_'}
    Building: {booking.room.building.name if booking.room and booking.room.building and booking.room.building.name is not None else '_'}
    ---

    """

    try:
        if user_email is not None:
            send_email(subject, message, recipients=[user_email])
        else:
            print("No email found for booking user")
    except Exception as e:
        print(f"Error sending email: {e}")

    # send to organization admins
    organization = booking.organization
    organisation_admins = UserOrganization.objects.filter(
        organization=organization, is_admin=True
    )

    admin_recipients = []
    for admin in organisation_admins:
        if admin.user.email is not None:
            admin_recipients.append(admin.user.email)

    try:
        if len(admin_recipients) > 0:
            send_email(subject, message, recipients=admin_recipients)
        else:
            print("No admin email found for organization")
    except Exception as e:
        print(f"Error sending email: {e}")

    print("Sent booking created email")


def send_booking_created_sms(booking_id: str):
    print("Sending SMS notification")
    pass


def send_booking_created_notification(booking_id: str):
    send_booking_created_email(booking_id)
    send_booking_created_sms(booking_id)
