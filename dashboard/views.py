from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from django.db import models
from teacher.models import Teacher,Subject
from course.models import Course,Batch
from student.models import Student
from main.models import User
from admission.models import StudentAdmission
from academics.models import AcademicConfig


class StatsViewSet(APIView):
    
    def get(self,request):    
        employee=Teacher.objects.count()
        student=Student.objects.count()
        course=Course.objects.count()
        batch=Batch.objects.count()

        output ={
            'count':{
                'employee':employee,
                'student':student,
                'course':course,
                'batch':batch
                },
            'academic':{}
        }

        configs = AcademicConfig.objects.all()
        for obj in configs:
             output['academic'][obj.name] = obj.value
            

        return Response(output)

