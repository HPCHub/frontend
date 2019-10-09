from django.db import models

# Create your models here.

class InviteEmailText(models.Model):
    title = models.TextField(
        null=False, blank=False,
        verbose_name='Email title'
    )
    body = models.TextField(
        null=False, blank=False,
        verbose_name='Email body',
        help_text='Your email address %s and your password %s'
    )

    class Meta:
        verbose_name = "Invitation email"
        verbose_name_plural = "Invitation emails"

    def __str__(self):
        return self.title


class RepeatedEmailText(models.Model):
    title = models.TextField(
        null=False, blank=False,
        verbose_name='Email title'
    )
    body = models.TextField(
        null=False, blank=False,
        verbose_name='Email body',
        help_text='Url for request = %'
    )

    class Meta:
        verbose_name = "Email on repeat"
        verbose_name_plural = "Emails on repeat"

    def __str__(self):
        return self.title

class MachineCredentialsEmailText(models.Model):
    title = models.TextField(
        null=False, blank=False,
        verbose_name='Email title'
    )
    body = models.TextField(
        null=False, blank=False,
        verbose_name='Email body',
        help_text='IP = %'
    )

    class Meta:
        verbose_name = "Email on repeat"
        verbose_name_plural = "Emails on repeat"

    def __str__(self):
        return self.title