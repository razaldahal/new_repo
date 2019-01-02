from django.db import models
from course.models import Course,Batch
from student.models import Student
from Section.models import Section
from Class.models import Class
# Create your models here.
from django.db import models
from main.models import *
# Create your models here.
class BusStaff(BaseModel):
    name=models.CharField(max_length=30)
    current_address=models.CharField(max_length=50)
    permanent_address=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=30)
    date_of_birth=models.DateField()
    license_no=models.CharField(max_length=20)
    #licence_valid_date=models.DateField()

    def __str__(self):
        return self.name


class Transport(BaseModel):
    driver=models.ForeignKey(BusStaff,on_delete=models.CASCADE)
    vehicle_no=models.CharField(max_length=20,unique=True)
    
    #route=models.ForeignKey(Route,on_delete=models.CASCADE)
    no_of_seats=models.IntegerField()
    max_allowed=models.IntegerField()
    insurance_renew_date=models.DateField()
    #contact_person=models.ForeignKey(User,on_delete=models.CASCADE)
    contact_person=models.CharField(max_length=40)
    def __str__(self):
        return "Vehicle_No"+":"+self.vehicle_no

from transport.models import Transport
class Route(BaseModel):
    start_location=models.CharField(max_length=30)
    stop_location=models.CharField(max_length=30)
    start_time=models.TimeField()
    vehicle=models.ForeignKey(Transport,on_delete=models.CASCADE)
    fee_amount=models.IntegerField()    
    def __str__(self):
        return self.start_location+" to "+self.stop_location

class TransportAllocation(BaseModel):
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    _class=models.ForeignKey(Class,on_delete=models.CASCADE)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    route=models.ForeignKey(Route,on_delete=models.CASCADE)


