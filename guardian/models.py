from django.db import models
from main.models import BaseModel, User
from student.models import Student


GUARDIAN_TYPE =(
	(1,'FATHER'),
	(2,'MOTHER'),
	(3,'LOCAL')
	)

class Guardian(BaseModel):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	type = models.CharField(choices=GUARDIAN_TYPE,max_length=7)

class GuardianStudent(BaseModel):
	guardian = models.ForeignKey(Guardian,on_delete=models.CASCADE)
	student = models.ForeignKey(Student,on_delete=models.CASCADE)


