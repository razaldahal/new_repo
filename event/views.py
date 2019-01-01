from django.shortcuts import render

# Create your views here.
from .serializers import *
from .models import *
from rest_framework import viewsets,status
from rest_framework.response import Response



class EventViewSet(viewsets.ModelViewSet):
    queryset=Event.objects.all()
    serializer_class=EventSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Event.objects.get_or_create(name=data['name'],description=data['description'],manager=Teacher.objects.get(id=data['manager']),progress=data['progress'],status=data['status'],date_start=data['date_start'],date_end=data['date_end'])
            if not b:
                return Response({'Detail':'Event already exists'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Deatil':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'name':obj.name,
            'description':obj.description,
            'progress':obj.progress,
            'manager':obj.manager.user.first_name+" "+obj.manager.user.last_name,
            'status':obj.status,
            'date_start':obj.date_start,
            'date_end':obj.date_end
            }
            output.append(temp)

        return Response(temp)

    def retrieve(self,request,pk):
        try:
            obj=Event.objects.get(id=pk)
        except:
            return Response({'Detail':'Event not Found!'},status=status.HTTP_404_NOT_FOUND)
        temp={'name':obj.name,
            'description':obj.description,
            'progress':obj.progress,
            'manager':obj.manager.user.first_name+" "+obj.manager.user.last_name,
            'status':obj.status,
            'date_start':obj.date_start,
            'date_end':obj.date_end
            }
        return Response(temp)    

    def update(self,request,pk):
        try:
            obj=Event.objects.get(id=pk)
        except:
            return Response({'Detail':'Event not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            obj.name=data['name']
            obj.description=data['description']
            obj.progress=data['progress']
            obj.status=data['status']
            obj.date_start=data['date_start']
            obj.date_end=data['date_end']
            obj.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,requets,pk):
        try:
            obj=Event.objects.get(id=pk)
        except:
            return Response({'Detail':'Event not Found!'},status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({'Success!':'Event Deleted'},status=status.HTTP_204_NO_CONTENT)    




