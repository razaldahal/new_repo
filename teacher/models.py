from django.db import models
from main.models import BaseModel,User,Phone,Address
#from course.models import Course,Batch
#from student.models import Student

class Teacher(BaseModel):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	qualification = models.CharField(max_length=120)

	def __str__(self):
		return self.user.first_name+" "+self.user.last_name



class Subject(BaseModel):
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=120)
	code=models.CharField(max_length=15)
	
	def __str__(self):
		return self.name


class Resources(BaseModel):
	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=120)
	#attachment =====

EXAM_TYPE =(
	('CLASS_TEST',1),
	('FIRST_TERMINAL',2),
	('SECOND_TERMINAL',3),
	('PRE_BOARD',4),
	('BOARD',5)
	)

class Test(BaseModel):
	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
	date = models.DateField()
	type = models.IntegerField(choices=EXAM_TYPE)
	full_marks = models.IntegerField()
	pass_marks = models.IntegerField()
