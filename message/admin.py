from django.contrib import admin

from .models import Message_Detail,Message
admin.site.register(Message_Detail)

admin.site.register(Message)