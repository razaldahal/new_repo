from django.db import models

from main.models import BaseModel

class School(BaseModel):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Department(BaseModel):
	school = models.ForeignKey(School,on_delete=models.CASCADE)
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=120)

	def __str__(self):
		return self.name
	

class Course(BaseModel):
	department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True)
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=120)
	code = models.CharField(max_length=16)
	#syllabus_name=models.CharField(max_length=100)

	def __str__(self):
		return self.name
	
class Batch(BaseModel):
	course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True)
	name = models.CharField(max_length=30)
	start_date=models.DateField()
	end_date=models.DateField()
	max_no_of_students=models.IntegerField()

	def __str__(self):
		return self.name
	