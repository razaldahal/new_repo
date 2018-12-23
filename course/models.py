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

	def __str__(self):
		return self.name
	