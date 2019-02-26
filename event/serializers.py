from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from academic.serializers import FacultySerializer
from .models import *


class EventTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = EventType
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=EventType.objects.all(),
                fields=('name', ),
                message=('This event type already exists.')
            )
        ]
            

class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'


class EventGetSerializer(serializers.ModelSerializer):
    type = EventTypeSerializer()
    manager = FacultySerializer()

    class Meta:
        model = Event
        fields = '__all__'