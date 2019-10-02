from django.core.mail import send_mail
from core.models import InviteEmailText, RepeatedEmailText
from django.conf import settings

def send_credentials_mail(pwd, email, request_url):
    invitation = InviteEmailText.objects.last()
    send_mail(
        invitation.title,
        invitation.body % (email, pwd, request_url),
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def send_repeated_mail(email, request_url):
    mail = RepeatedEmailText.objects.last()
    send_mail(
        mail.title,
        mail.body % request_url,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
