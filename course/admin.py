from django.contrib import admin

from .models import Course,Department,School,Batch

admin.site.register(Course)
admin.site.register(Department)
admin.site.register(School)
admin.site.register(Batch)