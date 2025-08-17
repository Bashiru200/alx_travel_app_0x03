from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_confirmation(email, booking_ref):
    subject = "Payment Confirmation"
    message = f"Your payment for booking {booking_ref} was successful!"
    send_mail(subject, message, "noreply@travelapp.com", [email])
