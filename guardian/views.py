
from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from student.models import Student
from main.models import User,GENDER,Phone,Address
from .models import Guardian,GuardianStudent
from main.models import GENDER
from main.helpers.tuple import get_choice_string
from .serializers import GuardianSerializer,GuardianStudentSerializer
from django.contrib.contenttypes.models import ContentType
from admission.serializers import *

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
											'username':ud['email'],
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

			c = ContentType.objects.get_for_model(user)
			Phone.objects.get_or_create(content_type=c,
										object_id=user.id,
										number=data['phone_detail']['number'],
										type=data['phone_detail']['type']
										)
			Address.objects.get_or_create(
										content_type=c,object_id=user.id,
										defaults={
										'province':data['address_detail']['province'],
										'district':data['address_detail']['district'],
										'city':data['address_detail']['city'],
										'address':data['address_detail']['address']
										}
										)

			Guardian.objects.get_or_create(user_id=user.id,
								defaults={'type':data['guardian_type']
								})
			return Response(serializer.data,status=status.HTTP_201_CREATED)

		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})
	def list(self,request): 
		objects = Guardian.objects.all()

		output = []
	
		for obj in objects:
			user=obj.user
			c=ContentType.objects.get_for_model(user)
			address=Address.objects.get(content_type=c,object_id=user.id)
			phone=Phone.objects.get(content_type=c,object_id=user.id,type=1)
		
			temp = {
				'id':obj.user.id,
				'name':obj.user.first_name+" "+obj.user.last_name,
				'email':obj.user.email,
				'gender':user.gender

								
				}
			temp['gender'] = get_choice_string(GENDER, user.gender)
			temp['address_detail']=AddressSerializer(address).data
			temp['phone_detail']=PhoneSerializer(phone).data

	
			output.append(temp)
		return Response(output)
	def retrieve(self,request,pk):
		guardian=Guardian.objects.get(id=pk)
		user=guardian.user
		c=ContentType.objects.get_for_model(user)
		address=Address.objects.get(content_type=c,object_id=user.id)
		phone=Phone.objects.get(content_type=c,object_id=user.id,type=1)
		temp={'name':guardian.user.first_name+" "+guardian.user.last_name,
			'email':guardian.user.email,
			'gender':guardian.user.gender
			}
		temp['address_detail']=AddressSerializer(address).data
		temp['phone_detail']=PhoneSerializer(phone).data	
		return Response(temp)
	def update(self,request,pk):
		guardian=Guardian.objects.get(id=pk)
		user=guardian.user
		c=ContentType.objects.get_for_model(user)
		address=Address.objects.get(content_type=c,object_id=user.id)
		phone=Phone.objects.get(content_type=c,object_id=user.id,type=1)
		serializer=GuardianSerializer(data=request.data)
		if serializer.is_valid():
			data=serializer.data
			guardian.type=data['guardian_type']
			address.province=data['address_detail']['province']
			address.city=data['address_detail']['city']
			address.district=data['address_detail']['district']
			address.address=data['address_detail']['address']
			address.save()
			phone.number=data['phone_detail']['number']
			phone.type=data['phone_detail']['type']
			phone.save()
			guardian.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)	
				
class GuardianStudentViewSet(viewsets.ModelViewSet):
	queryset = GuardianStudent.objects.all()
	serializer_class = GuardianStudentSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			gd = data['guardian']
			ud=gd['user']
			uemail=ud['email']
			guser = NotImplemented
			std = NotImplemented
			try:
				guser=User.objects.get(email=uemail)
			except:
				return redirect('/api/guardian/guardian/')
			try:
				std = Student.objects.get(id=data['student'])
			except:
				return Response('Student instance doesnt exist')	
	


			
	
			a = Guardian.objects.get(user=guser)
		
			

			b,c = GuardianStudent.objects.get_or_create(guardian=a,student=std)
			if c:
				return Response(data,status=status.HTTP_201_CREATED)
			else:
				return Response('This already exists')
		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})		


	def list(self,request):
		objects=self.queryset
		output=[]
		for obj in objects:
			temp = {
				'guardian':GuardianSerializer(obj.guardian).data,
				'student':StudentAdmissionGetSerializer(obj.student).data
			}
			output.append(temp)
		return Response(output) 