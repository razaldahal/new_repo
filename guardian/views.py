
from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from student.models import Student
from main.models import User,GENDER
from .models import Guardian,GuardianStudent
from main.models import GENDER
from main.helpers.tuple import get_choice_string
from .serializers import GuardianSerializer,GuardianStudentSerializer

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
			Guardian.objects.get_or_create(user_id=user.id,
								defaults={'type':data['guardian_type']
								})
			return Response(serializer.data,status=status.HTTP_201_CREATED)

		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})
	def list(self,request): 
		objects = self.queryset
		output = []
		
		for obj in objects:
		
			temp = {
				'id':obj.id,
				'name':obj.first_name+" "+obj.last_name,
				'email':obj.email,
				'gender':obj.gender
								
				}
			temp['gender'] = get_choice_string(GENDER, obj.gender)
			output.append(temp)
		return Response(output)
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
				'guardian':"user_id-->"+str(obj.guardian.user.id)+" , "+"guardian_id-->"+str(obj.guardian.id)+" , "+"full_name-->"+obj.guardian.user.first_name+" "+obj.guardian.user.last_name,
				'student':"user_id-->"+str(obj.student.user.id)+" , "+"student_id-->"+str(obj.student.user.id)+" , "+"full_name-->"+obj.student.user.first_name+" "+obj.student.user.last_name
			}
			output.append(temp)
		return Response(output) 