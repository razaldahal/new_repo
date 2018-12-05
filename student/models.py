from django.db import models
from main.models import User, BaseModel

from teacher.models import Test

class Student(BaseModel):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	registration_no = models.IntegerField()



from Section.models import SectionStudent
class TestStudent(BaseModel):
	section_student = models.ForeignKey(SectionStudent,on_delete=models.CASCADE)
	test = models.ForeignKey(Test,on_delete=models.CASCADE)
	mark_obtained = models.IntegerField()



