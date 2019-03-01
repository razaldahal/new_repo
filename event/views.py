from rest_framework.response import Response
from rest_framework import viewsets,status
import datetime
from datetime import timedelta


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

class EventNotificationViewSet(viewsets.ViewSet):
    queryset = Event.objects.all()

    def list(self,request):
        output = []
        t_n = {}
        today_date = datetime.datetime.now()
        # print('Today Date {}'.format(today_date))
        
        future_date = today_date + timedelta(days=7)
        # print(future_date)
       
        objects = self.queryset.filter(date_start__lte = future_date,date_end__gte=today_date)
        for obj in objects:
            temp = {
                'id':obj.id,
                'event':obj.name,
                'start_date':obj.date_start,
                'status':obj.status,
                'manager':obj.manager.user.first_name + ' ' + obj.manager.user.last_name,
                
                }
            output.append(temp)
            t_n['data'] = output
            t_n['count'] = len(output)
        return Response(t_n)