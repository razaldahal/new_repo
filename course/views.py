from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,viewsets,serializers
from .serializers import *
from .models import *
from django.core.exceptions import ValidationError

class SchoolViewset(viewsets.ModelViewSet):
    queryset=School.objects.all()
    serializer_class=SchoolSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            School.objects.update_or_create(name=data['name'])
            return Response(data)
        else:
            raise ValidationError({'Detail':[serializer.errors]})

class DepartmentViewset(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            Department.objects.get_or_create(school=School.objects.get(id=data['school']),name=data['name'],description=data['description'])
            return Response(data)
        else:
            raise ValidationError({'Detail':[serializer.errors]})

                






class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            e=Department.objects.get(id=data['department'])
            if not e:
                e=Department.objects.get(id=1)    
            obj,created =Course.objects.get_or_create(department=e,
            	name=data['name'],
            	description=data['description'],
                code=data['code'])
            #syllabus_name=data['syllabus_name'])

            if not created:
            	raise ValidationError({
	        	    'Detail':['Course Already Exist']
	       		    })
            else:
                return Response(data,status=status.HTTP_201_CREATED)
      

        else:
    	    raise ValidationError({
    		    'Detail':[serializer.errors]
        		})

    def retrieve(self,request,pk):
        try:
            instance = Course.objects.get(id=pk)
        except Exception as error:
            return Response(error)
        dict={
            'name':instance.name,
            'description':instance.description,
            'code':instance.code,
            'department':instance.department.name
        }
        return Response(dict)

    def list(self,request):
        object = self.queryset
        list=[]

        for obj in object:
            dct ={'id':obj.id,
            'department':obj.department.name,
            'name':obj.name,
            'code':obj.code
            }
            list.append(dct)

        return Response(list)



       
    
class BatchViewSet(viewsets.ModelViewSet):
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b = Batch.objects.get_or_create(course=Course.objects.get(id=data['course']),name=data['name'],start_date=data['start_date'],end_date=data['end_date'],max_no_of_students=data['max_no_of_students'])
            if not b:
                return Response('Batch already exists')
            else:
                return Response(data=data,status=status.HTTP_201_CREATED)
        else:
            raise ValidationError({'Detail':serializer.errors})

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={  
                    'id':obj.id,
                    'course':obj.course.name,
                    'name':obj.name,
                    'start_date':obj.start_date,
                    'end_date':obj.end_date,
                    'max_no_of_students':obj.max_no_of_students
                    }        
            output.append(temp)
        return Response(output)    
    
    def retrieve(self,request,pk):
        try:
            instance=Batch.objects.get(id=pk)
        except Exception as error:
            return Response(error)
        dict={
            'name':instance.name,
            'course':instance.course.name,
            'start_date':instance.start_date,
            'end_date':instance.end_date,
            'max_no_of_students':instance.max_no_of_students
        }
        return Response(dict)    