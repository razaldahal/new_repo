from .models import *
from rest_framework import serializers

class EventTypeserializer(serializers.Serializer):
    name=serializers.CharField()
class EventSerializer(serializers.Serializer):
    type=serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all())
    name=serializers.CharField()
    description=serializers.CharField()
    manager=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    date_start=serializers.DateField()
    date_end=serializers.DateField()
    progress=serializers.FloatField()
    status=serializers.CharField()

class EventTaskSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    name=serializers.CharField()
    description=serializers.CharField()
    status=serializers.CharField()
    priority = serializers.IntegerField()
    date = serializers.DateField()
    user = serializers.IntegerField()
    student = serializers.IntegerField()



    
