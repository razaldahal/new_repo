from .models import *
from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    type=serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all())
    name=serializers.CharField()
    description=serializers.CharField()
    manager=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    date_start=serializers.DateField()
    date_end=serializers.DateField()
    progress=serializers.FloatField()
    status=serializers.CharField()

class EevntTaskSerializer(serializers.Serializer):
    event=serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    name=serializers.CharField()
    description=serializers.CharField()
    status=serializers.CharField()

