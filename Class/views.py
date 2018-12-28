from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


from .models import Class
from .serializers import ClassSerializer

class ClassViewSet(viewsets.ModelViewSet):
	queryset = Class.objects.all()
	serializer_class = ClassSerializer
	
	def create(self,request):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			created,psk = Class.objects.get_or_create(name=data['name'],description=data['description'])
			if not psk:
				raise serializers.ValidationError({
					'detail':["Class Already Exist"]
					})

			return Response(data,status=status.HTTP_201_CREATED)

		else:
			raise serializers.ValidationError(
				{
				'Detail':[serializer.errors]
				})

	def list(self,request):
		objects=Class.objects.all()
		output=[]
		for obj in objects:
			temp={
				'id':obj.id,
				'name':obj.name,
				'description':obj.description
					}
			output.append(temp)
		return Response(output)				