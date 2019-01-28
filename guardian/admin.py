from django.contrib import admin

# Register your models here.
from .models import Guardian,GUARDIAN_TYPE,GuardianStudent
admin.site.register(Guardian)
admin.site.register(GuardianStudent)