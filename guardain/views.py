from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from main.models import User
from .models import Guardian
from .serializers import GuardianSerializer

class GuardianViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = GuardianSerializer
	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
		

			ud = data['user']
			user,val=User.objects.get_or_create(email=ud['email'],
											defaults={
											'first_name':ud['first_name'],
											'last_name':ud['last_name'],
											'gender':ud['gender'],
											'type':ud['type']
											})
			if not val:
				raise serializers.ValidationError(
					{
					'Detail':['Enter Unique Email']
					})
			Guardian.objects.get_or_create(user_id=user.id,
								defaults={'type':data['guardian_type']
								})
			return Response(serializer.data,status=status.HTTP_201_CREATED)

		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})


	def list(self,request):
		list =[]
		return Response(list)
