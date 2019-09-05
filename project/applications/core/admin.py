from django.contrib import admin
from .models import InviteEmailText, RepeatedEmailText
# Register your models here.

admin.site.register(InviteEmailText)
admin.site.register(RepeatedEmailText)