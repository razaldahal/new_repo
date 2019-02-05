from django.db import models


from student.models import BaseModel, Student


class BusStaff(BaseModel):
    name=models.CharField(max_length=30)
    current_address=models.CharField(max_length=50)
    permanent_address=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=30)
    date_of_birth=models.DateField()
    license_no=models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
    	db_table = 'transport_bus_staff'

class Transport(BaseModel):
    driver=models.ForeignKey(BusStaff,on_delete=models.CASCADE)
    vehicle_no=models.CharField(max_length=20,unique=True)

    no_of_seats=models.IntegerField()
    max_allowed=models.IntegerField()
    insurance_renew_date=models.DateField()
    contact_person=models.CharField(max_length=40)

    class Meta:
    	db_table = 'transport_transport'
    
    def __str__(self):
        return "Vehicle_No"+":"+self.vehicle_no


class Route(BaseModel):
    start_location=models.CharField(max_length=30)
    stop_location=models.CharField(max_length=30)
    start_time=models.TimeField()
    vehicle=models.ForeignKey(Transport,on_delete=models.CASCADE)
    fee_amount=models.FloatField()    

    class Meta:
    	db_table = 'transport_route'

    def __str__(self):
        return self.start_location

class TransportAllocation(BaseModel):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    route=models.ForeignKey(Route,on_delete=models.CASCADE)

    class Meta:
    	db_table = 'transport_bus_allocation'
  
