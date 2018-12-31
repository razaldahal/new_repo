from rest_framework import serializers
from .models import *
from admission.serializers import UserBaseSerializer,UserSerializer,USER_TYPE,PhoneSerializer,AddressSerializer
from course.models import Batch,Course
from Section.models import Section
from student.models import Student

class BusStaffSerializer(serializers.Serializer):
    name=serializers.CharField()
    license_no=serializers.CharField()
    permanent_address=serializers.CharField()
    current_address=serializers.CharField()
    phone_no=serializers.CharField()
    date_of_birth=serializers.DateField()
    # license_valid_date=serializers.DateField()
    # phone_detail=PhoneSerializer()
    # address_detail=AddressSerializer()
class RouteSerializer(serializers.Serializer):
    start_location=serializers.CharField()
    stop_location=serializers.CharField()
    start_time=serializers.TimeField()
    fee_amount=serializers.IntegerField()    
class TransportSerializer(serializers.Serializer):
    driver=serializers.PrimaryKeyRelatedField(queryset=BusStaff.objects.all())
    vehicle_no=serializers.CharField()
    #route=serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    no_of_seats=serializers.IntegerField()
    max_allowed=serializers.IntegerField()
    insurance_renew_date=serializers.DateField()
    contact_person=serializers.CharField(default='')
    #contact_person=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())    

class TransportAllocationSerializer(serializers.Serializer):
    batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    _class=serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    route=serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    section=serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())