from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from main.serializers import UserPostSerializer
from .models import *



  
class AcademicYearSerializer(serializers.ModelSerializer):
    #name = serializers.CharField(validators=[UniqueValidator(queryset=AcademicYear.objects.all())])
    class Meta:
        model = AcademicYear
        fields = ('name', 'is_active', 'date_start','date_end', 'description')
    


class CoursePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name','code','description')
    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','name','description','code')

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id','name', 'description')
   
class ClassPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('name', 'description',)
   

class SectionSerializer(serializers.ModelSerializer):
    _class = serializers.CharField(source='_class.name')
    class Meta:
        model = Section
        fields = ('id','name', '_class')
   
class SectionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('name', )



class FacultySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserPostSerializer()
    class Meta:
        model = Faculty
        fields = '__all__'
   