from django.shortcuts import render

# Create your views here.
from .serializers import *
from .models import *
from rest_framework import viewsets,status
from rest_framework.response import Response

class EventTypeViewSet(viewsets.ModelViewSet):
    queryset=EventType.objects.all()
    serializer_class=EventTypeserializer
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():

            data=request.data
            a,b=EventType.objects.get_or_create(data)
            if not b:
                return Response({'Detail':'Already exists!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)        
    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
                'name':obj.name}
            output.append(temp)
        return Response(output)            



class EventViewSet(viewsets.ModelViewSet):
    queryset=Event.objects.all()
    serializer_class=EventSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Event.objects.get_or_create(type=EventType.objects.get(id=data['type']),name=data['name'],description=data['description'],manager=Teacher.objects.get(id=data['manager']),progress=data['progress'],status=data['status'],date_start=data['date_start'],date_end=data['date_end'])
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

            temp={'id':obj.id,
            'type':obj.type.name,
            'name':obj.name,
            'description':obj.description,
            'progress':obj.progress,
            'manager':obj.manager.user.first_name+" "+obj.manager.user.last_name,
            'status':obj.status,
            'date_start':obj.date_start,
            'date_end':obj.date_end
            }
            output.append(temp)

        return Response(output)

    def retrieve(self,request,pk):
        try:
            obj=Event.objects.get(id=pk)
        except:
            return Response({'Detail':'Event not Found!'},status=status.HTTP_404_NOT_FOUND)
        temp={'type':obj.type.name,
            'name':obj.name,
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
            obj.type=EvnetType.objects.get(id=data['type'])
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


class EventTaskViewset(viewsets.ModelViewSet):
    serializer_class=EevntTaskSerializer
    queryset=EventTask.objects.all()

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=EevntTask.objects.get_or_create(event=Event.objects.get(id=data['event']),name=data['name'],status=data['status'],description=data['description'])
            if not b:
                return Response({'Detail':'EventTask already created!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'event':obj.event.name,
            'name':obj.name,
            'description':obj.description,
            'status':obj.status
            }
            output.append(temp)
        return Response(output)

    def retrieve(self,request,pk):
        try:
            et=EventTask.objects.get(id=pk)
        except:
            return Response({'Detail':'EventTask not found!'},status=status.HTTP_404_NOT_FOUND)
        temp={'name':et.name,
        'event':et.event.name,
        'description':et.description,
        'status':et.status
        }        
        return Response(temp)
    def update(self,request,pk):
        try:
            et=EevntTask.objects.get(id=pk)
        except:
            return Response({'Detail':'EventTask not found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            et.name=data['name']
            et.event=Event.objects.get(id=data['event'])
            et.description=data['description']
            et.status=data['status']
            et.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            et=EventTask.objects.get(id=pk)
        except:
            return Response({'Detail':'EventTask not found!'},status=status.HTTP_404_NOT_FOUND)
        et.delete()
        return Response({'Success!':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
                
