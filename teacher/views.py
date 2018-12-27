from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from student.models import Student
from course.models import Course,Batch
from main.models import User,Phone,Address
from assignment.models import Assignment
from .models import *
from Section.models import TeacherSection
from admission.serializers import UserGetSerializer,AddressSerializer,PhoneSerializer
from .serializers import TeacherAddSerializer,TeacherUpdateSerializer,SubjectSerializer,AssignmentSerializer,TeacherDetailAssignment,SubjectDetailAssignment,AssignmentDetail,ResourcesSerializer,ResourceDetailSerializer,TestSerializer


class TeacherViewSet(viewsets.ModelViewSet):
	queryset = Teacher.objects.all()
	serializer_class = TeacherAddSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			usr = data['user_detail']
			user,val = User.objects.get_or_create(email=usr['email'],
													defaults={
													'username':usr['email'],
													'first_name':usr['first_name'],
													'last_name':usr['last_name'],
													'type':2,
													'gender':usr['gender']
													})
			if not val:
				raise serializers.ValidationError({
					'Detail':['Enter Unique Email Address']
					})
			Teacher.objects.get_or_create(user_id=user.id,defaults={
										'qualification':data['qualification']
										})

			c = ContentType.objects.get_for_model(user)

			phone = data['phone_detail']
			Phone.objects.get_or_create(content_type=c,
										object_id=user.id,
										defaults={
										'type':phone['type'],
										'number':phone['number']
										})
			address = data['address_detail']
			Address.objects.get_or_create(content_type=c,
										 object_id=user.id,
										 defaults={
										 'district':address['district'],
										 'city':address['city'],
										 'province':address['province'],
										 'address':address['address']
										 }
										 )

			return Response(data)
		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})
	def list(self,request):
		objects = self.queryset
		output = []

		for obj in objects:
			user = obj.user
			c = ContentType.objects.get_for_model(user)
			address = Address.objects.get(content_type=c,object_id=user.id)
			phone = Phone.objects.get(content_type=c,object_id=user.id)

			temp={
			'id':obj.user.id

			}

			temp['user'] = UserGetSerializer(user).data
			temp['address_detail'] = AddressSerializer(address).data
			temp['phone_detail'] = PhoneSerializer(phone).data

			output.append(temp)



		return Response(output)


	def retrieve(self,request,pk):	
		teacher=Teacher.objects.get(id=pk)
		user=teacher.user
		c=ContentType.objects.get_for_model(user)
		address=Address.objects.get(content_type=c,object_id=user.id)
		phone=Phone.objects.get(content_type=c,object_id=user.id)
		temp={'id':teacher.id}
		temp['user']=UserGetSerializer(user).data
		temp['address_detail']=AddressSerializer(address).data
		temp['phone_detail']=PhoneSerializer(phone).data
		return Response(temp)
	
	def update(self,request,pk):
		teacher=Teacher.objects.get(id=pk)
		user=teacher.user
		c=ContentType.objects.get_for_model(user)
		address=Address.objects.get(content_type=c,object_id=user.id)
		phone=Phone.objects.get(content_type=c,object_id=user.id,type=1)

		serializer=TeacherUpdateSerializer(data=request.data)
		
		if serializer.is_valid():
			data=serializer.data
			print(data)
			teacher.qualification=data['qualification']

			address.province=data['address_detail']['province']
			address.city=data['address_detail']['city']
			address.district=data['address_detail']['district']
			address.address=data['address_detail']['address']
			address.save()
			phone.number=data['phone_detail']['number']
			phone.type=data['phone_detail']['type']
			phone.save()
			
			
			
			teacher.save()
			
			return Response(serializer.data)
		else:
			return Response(serializer.errors)



class SubjectViewSet(viewsets.ModelViewSet):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data

			sub,val = Subject.objects.get_or_create(name=data['name'],code=data['code'],
												defaults={
												'description':data['description']
												})
			if not val:
				raise serializers.ValidationError({
					'Detail':['This Book Is Already Exist']
					})
			return Response(serializer.data)

		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})

	def update(self,request,pk):
		subject=Subject.objects.get(id=pk)
		serializer=self.get_serializer(data=request.data)

		if serializer.is_valid():
			data=serializer.data
			subject.name=data['name']
			subject.code=data['code']
			subject.description=data['description']
			subject.save()
		return Response(data,status=status.HTTP_200_OK)
	def delete(self,request,pk):
		subject=Subject.objects.get(id=pk)
		serializer=self.get_serializer(data=request.data)
		if serializer.is_valid():
			subject.delete()
		return Response('Deleted Subject instance succesfully')	


class AssignmentViewSet(viewsets.ModelViewSet):
	queryset = Assignment.objects.all()
	serializer_class = AssignmentSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data=serializer.data
			ts = data['teacher_section_id']
			teacher_section_id = TeacherSection.objects.filter(id=ts)
			if teacher_section_id:
				Assignment.objects.get_or_create(teacher_section=teacher_section_id[0],
												defaults={
												'due_date':data['due_date'],
												'priority':data['priority'],
												'status':data['status'],
												'name':data['name'],
												'description':data['description']
												})
				return Response(data)
			else:
				raise serializers.ValidationError({
					'Detail':['TeacherSection id not Exist in database']
					})
		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})

	def list(self,request):
		print("list")
		objects = self.queryset
		output = []
		for obj in objects:
			teacher = obj.teacher_section.teacher.user
			subject = obj.teacher_section.subject
			
			temp ={
			
			
			}

			temp['teacher_detail'] = TeacherDetailAssignment(teacher).data
			temp['subject_detail'] = SubjectDetailAssignment(subject).data
			temp['Assignment_Detail'] = AssignmentDetail(obj).data
			output.append(temp)
		return Response(output)



class ResourcesViewSet(viewsets.ModelViewSet):
	queryset = Resources.objects.all()
	serializer_class = ResourcesSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			teacher = data['teacher_id']
			teacher = Teacher.objects.filter(id=teacher)
			if teacher:
				Resources.objects.get_or_create(teacher=teacher.first(),
												defaults={
												'name':data['name'],
												'description':data['description']
												})
				return Response(data)
			else:
				raise serializers.ValidationError({
					'Detail':['Teacher Dont Exist,Please!! Register']
					})
		else:
			raise serializers.ValidationError({
				"Detail":[serializer.errors]
				})

	def list(self,request):
		objects = self.queryset
		output = []
		for obj in objects:
			teacher = obj.teacher.user
			temp ={

			}
			temp['teacher_detail'] = TeacherDetailAssignment(teacher).data
			temp['Resource_Detail'] = ResourceDetailSerializer(obj).data
			output.append(temp)
		return Response(output)

class TestViewSet(viewsets.ModelViewSet):
	queryset = Test.objects.all()
	serializer_class = TestSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			teacher_id = data['teacher_id']
			teacher = Teacher.objects.filter(id=teacher_id)
			if teacher:
				Test.objects.get_or_create(teacher=teacher.first(),
										defaults={
										'date':data['date'],
										'type':data['type'],
										'full_marks':data['full_marks'],
										'pass_marks':data['pass_marks']
										})
				return Response(data)
			else:
				raise serializers.ValidationError({
					'Detail':['Teacher Not Exist']
					})

		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})
	def list(self,request):
		print("lists")
		objects = self.queryset
		output = []
		for obj in objects:

			temp = {
			'date':obj.date,
			'Exam_type':obj.type,
			'full_marks':obj.full_marks,
			'pass_marks':obj.pass_marks
			}
			output.append(temp)

		return Response(output)

