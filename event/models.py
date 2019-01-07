from django.db import models
from main.models import BaseModel
from teacher.models import Teacher
# Create your models here.

class EventType(BaseModel):
    name=models.CharField(max_length=100)
class Event(BaseModel):
    type=models.ForeignKey(EventType,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    progress=models.FloatField()  
    manager=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    status=models.CharField(max_length=50)
    date_start=models.DateField()
    date_end=models.DateField()


class EventTask(BaseModel):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    

    