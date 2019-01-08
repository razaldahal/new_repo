from django.db import models
from django.contrib.contenttypes.models import ContentType

from main.models import BaseModel, User
from academic.models import AcademicYear, Class, Section

class Student(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE, unique=True)
    registration_no = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'student_student'
        verbose_name_plural = "Student"

    def __str__(self):
        return self.registration_no

class Guardian(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type=models.CharField(max_length=10)
    name=models.CharField(max_length=100)
    mobile=models.CharField(max_length=20, null=True, blank=True)
    job=models.CharField(max_length=30, null=True, blank=True)
    citizenship_no=models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'student_parent'
        verbose_name_plural = "Guardian"

    def __str__(self):
        return self.name

# A student should be related to a section->class->course per academic year
class StudentEnroll(BaseModel):
    academic_year = models.ForeignKey(AcademicYear,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    _class = models.ForeignKey(Class,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE, null=True, blank=True)

    admission_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'student_enroll'
        verbose_name_plural = "StudentEnroll"

    def __str__(self):
        return str(self.academic_year.name) + ' ' + self.student.registration_no