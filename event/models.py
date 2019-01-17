from django.db import models
from main.models import BaseModel,User
from teacher.models import Teacher
from student.models import Student
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

PRIORITY =(
    (1,'HIGHEST'),
    (2,'HIGH'),
    (3,'NORMAL'),
    (4,'LOW')
)
class EventTask(BaseModel):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    status=models.CharField(max_length=50)
    priority = models.IntegerField(choices=PRIORITY)
    date = models.DateField()
    user_type = models.IntegerField()
    #user =  models.ForeignKey(User,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)


    