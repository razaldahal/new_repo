from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,viewsets,serializers
from .serializers import *
from .models import Course


class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            obj,created=Course.objects.get_or_create(department_id=data['department'],
            	name=data['name'],
            	description=data['description'])
            if not obj:
            	raise ValidationError({
	           		'Detail':['Course Already Exist']
	           		})
            return Response(data,status=status.HTTP_404_CREATED)

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
            'description':instance.description
        }
        return Response(dict)

    def list(self,request):
        object = self.queryset
        list=[]
        for obj in object:
            dct = CourseGetSerializer(obj).data
            list.append(dct)

        return Response(list)



       
    



