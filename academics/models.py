from django.db import models
from main.models import BaseModel
from teacher.models import Teacher,Subject
from Section.models import Section
# Create your models here.
class Timetable(BaseModel):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    start_time=models.TimeField()
    end_time=models.TimeField()
    week_day=models.DateField()


class AcademicConfig(BaseModel):
    name=models.CharField(max_length=50)
    value=models.CharField(max_length=50)

    
