from django.contrib import admin
from .models import TransportAllocation,BusStaff,Route,Transport
# Register your models here.
admin.site.register(Transport)
admin.site.register(TransportAllocation)
admin.site.register(BusStaff)
admin.site.register(Route)