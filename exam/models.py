from django.db import models
from main.models import BaseModel
from academic.models import Course,Class,Section
from student.models import Student

class ExamTerm(BaseModel):
    name = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    _class = models.ForeignKey(Class,on_delete=models.CASCADE)


class Subject(BaseModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    code=models.CharField(max_length=15)

    # def __str__(self):
    #     return self.name


class ExamSchedule(BaseModel):
    exam = models.ForeignKey(ExamTerm,on_delete=models.CASCADE,null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
class MarksEntry(BaseModel):
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamTerm,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)



class MarksEntryDetail(BaseModel):
    marks_entry = models.ForeignKey(MarksEntry,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    theory = models.IntegerField()
    practical = models.IntegerField()
    discipline = models.IntegerField()
    full_marks = models.IntegerField()
    full_marks_th = models.IntegerField()
    full_marks_pr = models.IntegerField()
    pass_marks = models.IntegerField()
    pass_marks_th = models.IntegerField()
    pass_marks_pr  = models.IntegerField()

    def __str__(self):
        return self.student.user.first_name