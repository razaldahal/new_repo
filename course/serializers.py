from rest_framework import serializers
from .models import *


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

# class BatchSerializer(serializers.Serializer):
#    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#    name=serializers.CharField()
#    start_date=serializers.DateField()
#    end_date=serializers.DateField()
#    max_no_of_students=serializers.IntegerField()

# class BatchGetSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=Batch
#         fields=('id','course','name','start_date','end_date','max_no_of_students')

# class AssignSubjectSerializer(serializers.Serializer):
#     course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#     batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
#     subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
# class SubjectAllocationSerializer(serializers.Serializer):
#     course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#     batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
#     subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
#     teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())        
# class ElectiveSubjectSerializer(serializers.Serializer):
#     course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#     batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
#     subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
#     student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())      

# class ClassTeacherAllocationSerializer(serializers.Serializer):
#     course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#     batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
#     section=serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
#     class_teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all()) 


# class ClassSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=Class
#         fields=('id','name','description')



# class SectionSerializer(serializers.Serializer):
#     _class =  serializers.IntegerField()
#     name = serializers.CharField()

# class SectionStudentSerializer(serializers.Serializer):
#     student_id = serializers.IntegerField()
#     section_id = serializers.IntegerField()
#     roll_no = serializers.IntegerField()

# class TeacherSectionSerializer(serializers.Serializer):
#     subject_id = serializers.IntegerField()
#     section_id = serializers.IntegerField()
#     teacher_id = serializers.IntegerField()

# class SectionRoutineSerializer(serializers.Serializer):
#     teacher_section_id = serializers.IntegerField()
#     day_of_week = serializers.DateField()
#     start_time = serializers.TimeField()
#     end_time = serializers.TimeField()            