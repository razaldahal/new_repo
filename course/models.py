from django.db import models
from teacher.models import Subject,Teacher
from main.models import BaseModel
from student.models import Student

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
	department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True)
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

class AssignSubject(BaseModel):
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)

class SubjectAllocation(BaseModel):
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
class ElectiveSubject(BaseModel):
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
