from django.contrib import admin

from .models import Course,Department,School

admin.site.register(Course)
admin.site.register(Department)
admin.site.register(School)