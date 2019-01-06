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
    theory_fm=serializers.IntegerField()
    theory_pm=serializers.IntegerField()
    practical_fm=serializers.IntegerField()
    pratical_pm=serializers.IntegerField()
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())