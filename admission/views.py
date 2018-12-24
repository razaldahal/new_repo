from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser

from main.models import User,Address,Phone,UserDetail
from student.models import Student
from guardain.models import Guardian, GuardianStudent
from .models import StudentAdmission
from .serializers import StudentAdmissionSerializer
#from main.helpers.parser import NestedMultipartParser



class StudentAdmissionViewSet(viewsets.ModelViewSet):
	queryset = StudentAdmission.objects.all()
	serializer_class = StudentAdmissionSerializer
	#parser_classes = (MultiPartParser,)



	def get(self, request):
		return Response([])
	def list(self, request):
		return Response([])

	def create(self,request):
		serializer = self.get_serializer(data=request.data)


		if serializer.is_valid():
			data = serializer.data
			ud = data['user']

			user,b = User.objects.get_or_create(
				email=ud['email'],
				defaults={
					'username':ud['email'],
					'first_name':ud['first_name'],
					'last_name':ud['last_name'],
					'gender':ud['gender'],
					'type':ud['type']
					}
				)
			if not b:
				raise serializers.ValidationError({
					'detail':["Email Already Exist"]
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

			detail = data.get('user_detail', False)
			if detail:
				UserDetail.objects.get_or_create(user_id=user.id,
												defaults={
												'blood_group':detail.get('blood_group',''),
												'nationality':detail.get('nationality',''),
												'mother_tongue':detail.get('mother_tongue',''),
												'religion':detail.get('religion',''),
												'citizenship_no':detail.get('citizenship_no',''),
												}
												)

			student,bval = Student.objects.get_or_create(user_id=user.id,registration_no=data['registration_no'])

			StudentAdmission.objects.get_or_create(student_id=student.id,
												   defaults={
												   'batch':data['batch'],
												   'course_id':data['course'],
												   'description':data['description'],
												   #'image':data['image']
												   }
												   )

			# father = data.get('father', False)
			# if father:
			# 	g = Guardian.objects.get_or_create()

			return Response(data,status=status.HTTP_201_CREATED)

		else:
			raise serializers.ValidationError({
					'detail':serializer.errors
					})