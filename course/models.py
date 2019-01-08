from django.db import models
from main.models import BaseModel

class Course(BaseModel):
	name = models.CharField(max_length=120)
	code = models.CharField(max_length=16)
	description = models.CharField(max_length=120)
	
	def __str__(self):
		return self.name


# class Class(BaseModel):
# 	course = models.ForeignKey(Course,on_delete=models.CASCADE)
# 	name = models.CharField(max_length=11)
# 	description = models.TextField()

# 	def __str__(self):
# 		return self.name


# class Section(BaseModel):
# 	_class=models.ForeignKey(Class,on_delete=models.CASCADE)
# 	name=models.CharField(max_length=120)

# 	def __str__(self):
# 		return self.name




# # class SectionRoutine(BaseModel):
# # 	teacher_section = models.ForeignKey(TeacherSection,on_delete=models.CASCADE)
# # 	day_of_week = models.CharField(max_length=120)
# # 	start_time = models.TimeField()
# # 	end_time = models.TimeField()




	
# # class Batch(BaseModel):
# # 	course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True)
# # 	name = models.CharField(max_length=30)
# # 	start_date=models.DateField()
# # 	end_date=models.DateField()
# # 	max_no_of_students=models.IntegerField()

# # 	def __str__(self):
# # 		return self.name

# class AssignSubject(BaseModel):
# 	_class=models.ForeignKey(Class,on_delete=models.CASCADE)
# 	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)

# class SubjectAllocation(BaseModel):
# 	course=models.ForeignKey(Course,on_delete=models.CASCADE)
# 	_class=models.ForeignKey(Class,on_delete=models.CASCADE)
# 	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
# 	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)



# class ElectiveSubject(BaseModel):
# 	_class=models.ForeignKey(Class,on_delete=models.CASCADE)
# 	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
# 	student=models.ForeignKey(Student,on_delete=models.CASCADE)

# class ClassTeacherAllocation(BaseModel):
# 	course=models.ForeignKey(Course,on_delete=models.CASCADE)
# 	batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
# 	section=models.ForeignKey(Section,on_delete=models.CASCADE)
# 	class_teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
	
# 	