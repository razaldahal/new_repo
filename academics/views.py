from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.response import Response
import datetime
from datetime import date,time
class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class=TimetableSerializer
    queryset=Timetable.objects.all()
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            if data['set']:

                a,b=Timetable.objects.get_or_create(teacher=Teacher.objects.get(id=data['teacher']),section=Section.objects.get(id=data['section']),subject=Subject.objects.get(id=data['subject']),start_time=data['start_time'],end_time=data['end_time'],week_day=data['week_day'])
                if not b:
                    return Response({"Detail":"Already Added!"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data,status=status.HTTP_201_CREATED)            
        else:
            return Response(serializer.errors)
    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'teacher':obj.teacher.user.first_name+" "+obj.teacher.user.last_name,
            'section':obj.section._class.name+":"+obj.section.name,
            'day':obj.week_day.strftime("%A"),
            'start_time':obj.start_time,
            'end_time':obj.end_time,
            'subject':obj.subject.name
            }
            output.append(temp)
        return Response(output)

    def retrieve(self,request,pk):

        timetable=Timetable.objects.get(id=pk)   
        temp={'teacher':timetable.teacher.user.first_name+" "+timetable.teacher.user.last_name,
        'subject':timetable.subject.name,
        'section':timetable.section._class.name+":"+timetable.section.name,
        'week_day':timetable.week_day.strftime("%A"),
        'start_time':timetable.start_time,
        'end_time':timetable.end_time
        }
        return Response(temp)
    def update(self,request,pk):
        timetable=Timetable.objects.get(id=pk)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            if data['set']:
                timetable.teacher=Teacher.objects.get(id=data['teacher'])
                timetable.section=Section.objects.get(id=data['section'])
                timetable.subject=Subject.objects.get(id=data['subject'])
                timetable.week_day=data['week_day']
                timetable.start_time=data['start_time']
                timetable.end_time=data['end_time']
                timetable.save()
                return Response(data,status=status.HTTP_200_OK)
            elif not data['set']:
                timetable.delete()
                return Response({"Success!":"Deleted!"},status=status.HTTP_204_NO_CONTENT)    
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)            
    


# class AcademicConfigViewSet(viewsets.ViewSet):

#     queryset=AcademicConfig.objects.all()

#     def create(self,request):
#         data=request.data
#         a,b=AcademicConfig.objects.get_or_create(name=data['name'],value=data['value'])
#         if not b:
#             return Response({'Detail':'Config already exists!'},status=status.HTTP_400_BAD_REQUEST)

#         else:
#             return Response(data,status=status.HTTP_201_CREATED)

#     def list(self,request):
#         objects=self.queryset
#         output={}
#         for obj in objects:
#             output[obj.name] = obj.value
            
#         return Response(output)



    