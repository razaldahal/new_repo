from rest_framework import serializers
from .models import *
from teacher.models import Teacher
from Section.models import Section,Subject

class TimetableSerializer(serializers.Serializer):
    teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    section=serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    start_time=serializers.TimeField()
    end_time=serializers.TimeField()
    week_day=serializers.DateField()
    subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    set=serializers.BooleanField()