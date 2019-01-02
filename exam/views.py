from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import *
from .serializers import *

class TermViewset(viewsets.ModelViewSet):
    queryset=Term.objects.all()
    serializer_class=TermSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serialzer.data
            a,b=Term.objects.get_or_create(name=data['name'],start_date=data['start_date'],end_date=data['end_date'],batch=Batch.objects.get(id=data['batch']))
            if not b:
                return Response({'Term':'Already Created!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Error!':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'name':obj.name,
            'start_date':obj.start_date,
            'end_date':obj.end_date,
            'batch':obj.batch.name
            }
            output.append(temp)
        return Response(output)

    def retrieve(self,request,pk):
        try:
            term=Term.objects.get(id=pk)
        except:
            return Response({'Error':'Exam Term not found!'},status=status.HTTP_404_NOT_FOUND)
        temp={'name':term.name,
        'batch':term.batch.name,
        'start_date':term.start_date,
        'end_date':term.end_date
        }
        return Response(temp)
    def update(self,request,pk):
        try:
            trm=Term.objects.get(id=pk)
        except:
            return Response({'Error':'Exam Term not found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data 
            trm.name=data['name']
            trm.batch=Batch.objects.get(id=data['batch'])
            trm.start_date=data['start_date']
            trm.end_date=data['end_date']
            trm.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            trm=Term.objects.get(id=pk)
        except:
            return Response({'Error':'Exam Term not found!'},status=status.HTTP_404_NOT_FOUND)
        trm.delete()
        return Response({"Success!":"Deleted"},status=status.HTTP_204_NO_CONTENT)

class ScheduleViewset(viewsets.ModelViewSet):
    serializer_class=ScheduleSerializer
    queryset=Schedule.objects.all()

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Schedule.objects.get_or_create(subject=Subject.objects.get(id=data['subject']),term=Term.objects.get(id=data['term']),start_time=data['start_time'],end_time=data['end_time'])
            if not b:
                return Response({'Schedule':'Already Created'},status=status.HTTP_400_BAD_REQUEST)
            else:
                 return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'subject':obj.subject.name,
            'term':obj.term.name,
            'start_time':obj.start_time,
            'end_time':obj.end_time
            }
            output.append(temp)
        return Response(output)
    def retrieve(self,request,pk):
        try:
            s=Schedule.objects.get(id=pk)
        except:
            return Response({'Detail':'Schedule not found!'},status=status.HTTP_404_NOT_FOUND)
        temp={'subject':s.subject.name,
        'term':s.term.name,
        'start_time':s.start_time,
        'end_time':s.end_time
        }
        return Response(temp)

    def update(self,request,pk):
        try:
            s=Schedule.objects.get(id=pk)
        except:
            return Response({'Detail':'Schedule not found'},status=status.HTTP_404_NOT_FOUND)

        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            s.name=data['name']
            s.term=Term.objects.get(id=data['term'])
            s.start_time=data['start_time']
            s.end_time=data['end_time']
            s.subject=Subject.objects.get(id=data['subject'])
            s.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            s=Schedule.objects.get(id=pk)
        except:
            return Response({'Detail':'Schedule not found'},status=status.HTTP_404_NOT_FOUND)
        s.delete()
        return Response({'Success!':'Deleted'},status=status.HTTP_204_NO_CONTENT)         