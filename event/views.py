from rest_framework.response import Response
from rest_framework import viewsets,status


from .serializers import *


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return EventGetSerializer
        return EventSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()
