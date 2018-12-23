from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    department = serializers.IntegerField()

    class Meta:
        model=Course
        fields=('department','name','description')

class CourseGetSerializer(serializers.ModelSerializer):

    class Meta:
        model=Course
        fields=('id', 'department','name','description')