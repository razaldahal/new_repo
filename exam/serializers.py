from rest_framework import serializers
from .models import *

class TermSerializer(serializers.Serializer):
    name=serializers.CharField()
    batch=serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
    start_date=serializers.DateField()
    end_date=serializers.DateField()

class ScheduleSerializer(serializers.Serializer):
        subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
        term=serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
        start_time=serializers.TimeField()
        end_time=serializers.TimeField()
        date=serializers.DateField()

class MarksSerializer(serializers.Serializer):
    _class=serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    section=serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    exam=serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    theory_fm=serializers.IntegerField()
    theory_pm=serializers.IntegerField()
    practical_fm=serializers.IntegerField()
    practical_pm=serializers.IntegerField()
    
class StudentmarksSerializer(serializers.Serializer):
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    marks=serializers.PrimaryKeyRelatedField(queryset=Marks.objects.all())
    obtained_theory_marks=serializers.IntegerField()
    obtained_practical_marks=serializers.IntegerField()

class SectionsubjectSerializer(serializers.Serializer):
	section=serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
	subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())