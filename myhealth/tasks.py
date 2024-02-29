from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Appointment
from datetime import datetime, timedelta


@shared_task
def send_email_task():
    today = datetime.now().date()
    tomorrow = datetime.now().date() + timedelta(days=1)
    appointments = Appointment.objects.filter(date = tomorrow)

    for appointment in appointments:
        user = appointment.user
        print(user.email)
        to_email = [user.email]

        context = {
            'appointment': appointment,
            'user': user
        }

        html_body = render_to_string('myhealth/email_templates/appointment.html', context)

        message = EmailMultiAlternatives(
            subject = 'Upcoming appointment!',
            body = "Email testing",
            from_email = 'ha.le.developer@protonmail.com',
            to = to_email,
        )

        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently = False)
