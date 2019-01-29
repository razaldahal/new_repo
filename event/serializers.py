from .models import *
from rest_framework import serializers
from main.models import USER_TYPE

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
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    name=serializers.CharField()
    description=serializers.CharField()
    status=serializers.CharField()
    priority = serializers.IntegerField()
    date = serializers.DateField()
    user_type = serializers.ChoiceField(choices=USER_TYPE)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())



    
