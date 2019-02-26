from django.db import models
from main.models import BaseModel, User

## This tables handles all data for each academic year
class AcademicYear(BaseModel):
    name = models.CharField(max_length=120)
    date_start = models.DateField()
    date_end = models.DateField()
    description = models.TextField()
    is_active = models.BooleanField(default=False) # only 1 row/year should be True at a time.i.e. all other False

    class Meta:
        db_table = 'academic_year'
        verbose_name_plural = "AcademicYear"

    def __str__(self):
        return self.name

class Course(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=16)
    description = models.CharField(max_length=120)
    
    class Meta:
        db_table = 'academic_course'
        verbose_name_plural = "Course"

    def __str__(self):
        return self.name


class Class(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=11)
    description = models.TextField()

    class Meta:
        db_table = 'academic_class'
        verbose_name_plural = "Class"


    def __str__(self):
        return self.name


class Section(BaseModel):
    _class = models.ForeignKey(Class,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'academic_section'
        verbose_name_plural = "Section"


    def __str__(self):
        return self.name



class Faculty(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    qualification = models.TextField()
    
    class Meta:
        db_table = 'academic_faculty'
        verbose_name_plural = "Faculty"

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name




