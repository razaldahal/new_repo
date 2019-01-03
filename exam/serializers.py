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

