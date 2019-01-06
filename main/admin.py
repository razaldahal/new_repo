from django.contrib import admin
from .models import Parent,User,UserDetail,Phone,Address
# Register your models here.
admin.site.register(Parent)

admin.site.register(User)

admin.site.register(Phone)

admin.site.register(UserDetail)

admin.site.register(Address)