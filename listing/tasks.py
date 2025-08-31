from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_confirmation(email, booking_ref):
    subject = "Payment Confirmation"
    message = f"Your payment for booking {booking_ref} was successful!"
    send_mail(subject, message, "noreply@travelapp.com", [email])

@shared_task
def send_booking_confirmation(email, booking_ref):
    subject = "Booking Confirmation"
    message = f"Your booking {booking_ref} has been confirmed!"
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [email])