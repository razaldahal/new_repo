from django.db import models
from main.models import BaseModel
from teacher.models import Subject,Teacher
from course.models import Course,Batch
# Create your models here.


class Term(BaseModel):
    name=models.CharField(max_length=30)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()

class Schedule(BaseModel):
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    term=models.ForeignKey(Term,on_delete=models.CASCADE)
    start_time=models.TimeField()
    end_time=models.TimeField()
    date=models.DateField()

# EXAM_TYPE =(
# 	('CLASS_TEST',1),
# 	('FIRST_TERMINAL',2),
# 	('SECOND_TERMINAL',3),
# 	('PRE_BOARD',4),
# 	('BOARD',5)
# 	)

# class Test(BaseModel):
# 	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
# 	date = models.DateField()
# 	type = models.IntegerField(choices=EXAM_TYPE)
# 	full_marks = models.IntegerField()
# 	pass_marks = models.IntegerField()

