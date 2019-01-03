from rest_framework import serializers
from .models import *

class SchoolSerializer(serializers.Serializer):
    name=serializers.CharField()
class DepartmentSerializer(serializers.Serializer):
    school=serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    name=serializers.CharField()
    description=serializers.CharField()
class CourseSerializer(serializers.ModelSerializer):
    code=serializers.CharField(max_length=16)
    #department=serializers.CharField()
    class Meta:
        model=Course
        fields=('name','code','description')
    
class CourseGetSerializer(serializers.ModelSerializer):

    class Meta:
        model=Course
        fields=('id', 'department','name','description','code')

class BatchSerializer(serializers.Serializer):
   course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
   name=serializers.CharField()
   start_date=serializers.DateField()
   end_date=serializers.DateField()
   max_no_of_students=serializers.IntegerField()

class BatchGetSerializer(serializers.ModelSerializer):

    class Meta:
        model=Batch
        fields=('id','course','name','start_date','end_date','max_no_of_students')

class AssignSubjectSerializer(serializers.Serializer):
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
    subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
class SubjectAllocationSerializer(serializers.Serializer):
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
    subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())        
class ElectiveSubjectSerializer(serializers.Serializer):
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
    subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())      

class ClassTeacherAllocationSerializer(serializers.Serializer):
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
    class_teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all()) 