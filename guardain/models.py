from django.db import models
from main.models import BaseModel, User
from student.models import Student


GUARDIAN_TYPE =(
	('FATHER',1),
	('MOTHER',2),
	('LOCAL',3)
	)

class Guardian(BaseModel):
	# user = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	mobile = models.CharField(max_length=100)
	job = models.CharField(max_length=100)
	citizen_no = models.CharField(max_length=100)
	type = models.IntegerField(choices=GUARDIAN_TYPE)

class GuardianStudent(BaseModel):
	guardian = models.ForeignKey(Guardian,on_delete=models.CASCADE)
	student = models.ForeignKey(Student,on_delete=models.CASCADE)