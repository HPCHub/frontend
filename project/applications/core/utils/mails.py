from django.core.mail import send_mail
from core.models import InviteEmailText, RepeatedEmailText, MachineCredentialsEmailText
from django.conf import settings
from django.core.mail import EmailMessage


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

def send_machine_credentials_mail(user_mail, ip_data, key_data, single_id):
    mail = MachineCredentialsEmailText.objects.last()
    email = EmailMessage(
        mail.title,
        mail.body.format(ip_data),
        settings.DEFAULT_FROM_EMAIL,
        [user_mail],
    )
    with open('{}-key.txt'.format(single_id), 'rw') as key_file:
        key_file.write(key_data)
        key_file.close()
    email.attach('{}-key.txt'.format(single_id))
    email.send(fail_silently=False)
