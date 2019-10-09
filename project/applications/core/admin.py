from django.contrib import admin
from .models import InviteEmailText, RepeatedEmailText, MachineCredentialsEmailText
# Register your models here.

admin.site.register(InviteEmailText)
admin.site.register(RepeatedEmailText)
admin.site.register(MachineCredentialsEmailText)
