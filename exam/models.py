from django.db import models
from main.models import BaseModel
from teacher.models import Subject,Teacher
from course.models import Course,Batch
from Class.models import Class
from Section.models import Section
from student.models import Student
# Create your models here.


class Term(BaseModel):
    name=models.CharField(max_length=30)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()

class Schedule(BaseModel):
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    term=models.ForeignKey(Term,on_delete=models.CASCADE)
    start_time=models.TimeField()
    end_time=models.TimeField()
    date=models.DateField()

class Marks(BaseModel):
    _class=models.ForeignKey(Class,on_delete=models.CASCADE)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    exam=models.ForeignKey(Term,on_delete=models.CASCADE)
    theory_fm=models.IntegerField()
    theory_pm=models.IntegerField()
    practical_fm=models.IntegerField()
    practical_pm=models.IntegerField()
    full_marks=models.IntegerField()
    pass_marks=models.IntegerField()

class Studentmarks(BaseModel):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    marks=models.ForeignKey(Marks,on_delete=models.CASCADE)
    obtained_theory_marks=models.IntegerField()
    obtained_practical_marks=models.IntegerField()
    
class Sectionsubject(BaseModel):
	section=models.ForeignKey(Section,on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)


class Class(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=11)
    description = models.TextField()

    class Meta:
        db_table = 'exam_class'
        verbose_name_plural = "Class"


    def __str__(self):
        return self.name
