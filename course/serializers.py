from rest_framework import serializers
from .models import *

class SchoolSerializer(serializers.Serializer):
    name=serializers.CharField()
class DepartmentSerializer(serializers.Serializer):
    school=serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    name=serializers.CharField()
    description=serializers.CharField()
class CourseSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    code=serializers.CharField(max_length=16)
    class Meta:
        model=Course
        fields=('department','name','code','description')

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