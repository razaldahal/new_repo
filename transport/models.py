from django.db import models
from student.models import BaseModel, Student


class Staff(BaseModel):
    name=models.CharField(max_length=30)
    current_address=models.CharField(max_length=255)
    permanent_address=models.CharField(max_length=255, null=True)
    phone_number=models.CharField(max_length=30, null=True)
    date_of_birth=models.DateField(null=True)
    license_number=models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    class Meta:
    	db_table = 'transport_staff'

class Vehicle(BaseModel):
    staff=models.ForeignKey(Staff,on_delete=models.CASCADE)
    vehicle_no=models.CharField(max_length=20,unique=True)

    no_of_seats=models.IntegerField()
    max_allowed=models.IntegerField()
    insurance_renew_date=models.DateField()
    contact_person=models.CharField(max_length=40, null=True)
    start_location=models.CharField(max_length=30, null=True)
    stop_location=models.CharField(max_length=30, null=True)
    start_time=models.TimeField(null=True)

    class Meta:
    	db_table = 'transport_vehicle'
    
    def __str__(self):
        return "Vehicle_No"+":"+self.vehicle_no


class VehicleAllocation(BaseModel):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    fee_amount=models.FloatField(null=True)

    class Meta:
    	db_table = 'transport_vehicle_allocation'