from django.contrib import admin
from .models import Books,Issue_book,Request_book,Book_return
# Register your models here.
admin.site.register(Books)
admin.site.register(Issue_book)
admin.site.register(Request_book)
admin.site.register(Book_return)