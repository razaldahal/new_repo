from django.db import models

from main.models import BaseModel
from Class.models import Class
from student.models import Student
from teacher.models import Subject,Teacher



class Section(BaseModel):
	_class=models.ForeignKey(Class,on_delete=models.CASCADE)
	name=models.CharField(max_length=120)

	def __str__(self):
		return self.name


class SectionStudent(BaseModel):
	student = models.ForeignKey("student.student",on_delete=models.CASCADE)
	section = models.ForeignKey(Section,on_delete=models.CASCADE)
	roll_no = models.IntegerField()


class TeacherSection(BaseModel):
	subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
	section = models.ForeignKey(Section,on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)


class SectionRoutine(BaseModel):
	teacher_section = models.ForeignKey(TeacherSection,on_delete=models.CASCADE)
	day_of_week = models.CharField(max_length=120)
	start_time = models.TimeField()
	end_time = models.TimeField()



