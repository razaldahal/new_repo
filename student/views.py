from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from rest_framework import serializers

from admission.models import StudentAdmission
from admission.serializers import *
from main.models import UserDetail
from .models import Student,TestStudent
from main.models import Address,Phone,Parent
from assignment.models import Assignment,StudentAssignment
from Section.models import SectionStudent
from teacher.models import Test
from .serializers import StudentAssignmentSerializer,StudentAssignmentDetail,AssStdSectionSerializer,TestStudentSerializer,TestDetailGet



class StudentGetViewSet(viewsets.ModelViewSet):

	queryset = Student.objects.all()
	serializer_class = UserGetSerializer

	def list(self,request):
		output = []

		for adm in StudentAdmission.objects.all():
			user = adm.student.user
			c=ContentType.objects.get_for_model(user)
		
			address = Address.objects.get(content_type=c,object_id=user.id)
			phone = Phone.objects.get(content_type=c,object_id=user.id,type=1)
			father = Parent.objects.get(content_type=c,object_id=user.id,type='Father')
			mother = Parent.objects.get(content_type=c,object_id=user.id,type='Mother')



			admission_date = adm.admission_date

			tmp ={
			'id': adm.student.id,
			'admission_date':adm.admission_date.date(),
			'course':adm.course.name
			}

			tmp['user']  = UserGetSerializer(user).data
			
			ud = UserDetail.objects.filter(user_id=user.id)
			if ud:
				tmp['user_detail'] = UserDetailSerializer(ud.first()).data

			bst={

			}


			tmp['address_detail'] = AddressSerializer(address).data
			phone_data = PhoneSerializer(phone).data
			tmp['phone'] = phone_data
			
			tmp['parents']={
			'father':FatherSerializer(father).data,
			'mother':MotherSerializer(mother).data
			}


			output.append(tmp)

		return Response(output)

	def retrieve(self,request,pk):
		try:
			user_obj = StudentAdmission.objects.get(id=pk)
		except:
			raise serializers.ValidationError({
				'Detail':['This Id Doesnot Exist']
				})
		user = user_obj.student.user
		c=ContentType.objects.get_for_model(user)
	
		address = Address.objects.get(content_type=c,object_id=user.id)
		phone = Phone.objects.get(content_type=c,object_id=user.id,type=1)
		#parent = Parent.objects.get(content_type=c,object_id=user.id)
		father = Parent.objects.get(content_type=c,object_id=user.id,type='Father' )
		mother = Parent.objects.get(content_type=c,object_id=user.id,type='Mother')




		admission_date = user_obj.admission_date

		tmp ={
		'admission_id': user_obj.student.id,
		'admission_date':user_obj.admission_date.date(),
		'course':user_obj.course.name,
		'batch':user_obj.batch,
		'registration_no':user_obj.student.registration_no
		}

		tmp['user']  = UserGetSerializer(user).data
		
		ud = UserDetail.objects.filter(user_id=user.id)
		if ud:
			tmp['user_detail'] = UserDetailSerializer(ud.first()).data

		tmp['address_detail'] = AddressSerializer(address).data
		phone_data = PhoneSerializer(phone).data
		tmp['phone'] = phone_data
		#tmp['parent'] = ParentSerializer(parent).data
		tmp['parents']={
			'father':FatherSerializer(father).data,
			'mother':MotherSerializer(mother).data
			}

			
		return Response(tmp)

	def update(self,request,pk,format=None):
		user_obj=StudentAdmission.objects.get(student_id=pk)
		user = user_obj.student.user
		c=ContentType.objects.get_for_model(user)
	
		address = Address.objects.get(content_type=c,object_id=user.id)
		phone = Phone.objects.get(content_type=c,object_id=user.id,type=1)
		#parent = Parent.objects.get(content_type=c,object_id=user.id)
		father = Parent.objects.get(content_type=c,object_id=user.id,type='Father' )
		mother = Parent.objects.get(content_type=c,object_id=user.id,type='Mother')


	tmp ={
		
	}


		
class StudentAssignmentViewSt(viewsets.ModelViewSet):
	queryset = StudentAssignment.objects.all()
	serializer_class = StudentAssignmentSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data

			assignment = data['assignment_id']
			ass_obj= Assignment.objects.filter(id=assignment)

			sec_std = data['section_student_id']
			sec_obj = SectionStudent.objects.filter(id=sec_std)

			if ass_obj and sec_obj:
				assignment,val=StudentAssignment.objects.get_or_create(assignment=ass_obj.first(),
													defaults={
													'section_student':sec_obj.first(),
													'status':data['status']
													})
				if not val:
					raise serializers.ValidationError({
						"SORRY":['Student can submit per assignment only once']
						})

				return Response(data)
			else:
				raise serializers.ValidationError({
					"Detail":['Assignment Or Section Not Exist in DAtabase']
					})
		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})

	def list(self,request):
		objects = self.queryset
		output =  []
		for obj in objects:
			assignment = obj.assignment
			sec = obj.section_student.student.user
			temp={

			}
			temp['Assignment_Detail']=StudentAssignmentDetail(assignment).data
			temp['Student_Detail'] = AssStdSectionSerializer(sec).data
			output.append(temp)
		return Response(output)

class TestStudentViewSet(viewsets.ModelViewSet):
	queryset = TestStudent.objects.all()
	serializer_class = TestStudentSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			std_id = data['section_student_id']
			student = SectionStudent.objects.filter(id=std_id)
			test_id = data['test_id']
			test = Test.objects.filter(id=test_id)
			if student and test:
				TestStudent.objects.get_or_create(section_student=student[0],
													defaults={
													'test':test.first(),
													'mark_obtained':data['mark_obtained']
													})
				return Response(data)
			else:
				if not student:
					raise serializers.ValidationError({
							'Detail':["Student not Exist"]
							})
				raise serializers.ValidationError({
						'Detail':["This Test not Exist"]
						})
		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})

	def list(self,request):
		objects = self.queryset
		output = []
		for obj in objects:
			student = obj.section_student.student.user
			test = obj.test
			temp = {
			"mark_obtained":obj.mark_obtained

			}
			temp["student_detail"] = UserGetSerializer(student).data
			temp["test_detail"] = TestDetailGet(test).data
			output.append(temp)
		return Response(output)

	def retrieve(self,request,pk):
		try:
			instance = TestStudent.objects.get(id=pk)
		except:
			raise serializers.ValidationError({
				"Detail":['Enter Valid Student Id']
				})
	
		student = instance.section_student.student.user
		test = instance.test
		temp = {
		"mark_obtained":instance.mark_obtained

		}
		temp["student_detail"] = UserGetSerializer(student).data
		temp["test_detail"] = TestDetailGet(test).data
		return Response(temp)
	