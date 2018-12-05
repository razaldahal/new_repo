from django.db import models

from main.models import BaseModel
#from Section.models import TeacherSection
from Section.models import SectionStudent

STATUS=(
	('SUBMITTED',1),
	('PENDING',2)
	)


class Assignment(BaseModel):
#	teacher_section = models.ForeignKey(TeacherSection,on_delete=models.CASCADE)
	due_date = models.DateField()
	priority = models.CharField(max_length=120)
	status = models.IntegerField(choices=STATUS)
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=120)
	#attachment = -----



class StudentAssignment(BaseModel):
	assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
	section_student = models.ForeignKey(SectionStudent,on_delete=models.CASCADE)
	status = models.IntegerField(choices=STATUS)
	#attachment=====
