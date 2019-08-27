from django.core.mail import send_mail
from core.models import InviteEmailText
from django.conf import settings

def send_credentials_mail(pwd, email):
    invitation = InviteEmailText.objects.last()
    send_mail(
        invitation.title,
        invitation.body % (email, pwd),
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
