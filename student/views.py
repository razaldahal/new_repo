from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from rest_framework import serializers
from rest_framework import status
from admission.models import StudentAdmission
from admission.serializers import StudentUpdateSerializer,UserGetSerializer,UserDetailSerializer,PhoneSerializer,AddressSerializer,FatherSerializer,MotherSerializer,GuardianSerializer,SectionSerializer,TransportAllocationSerializer
from main.models import UserDetail
from .models import Student,TestStudent
from main.models import Address,Phone,Parent
from assignment.models import Assignment,StudentAssignment
from Section.models import SectionStudent
from teacher.models import Test
from .serializers import StudentAssignmentSerializer,StudentAssignmentDetail,AssStdSectionSerializer,TestStudentSerializer,TestDetailGet



class StudentGetViewSet(viewsets.ModelViewSet):

	queryset = Student.objects.all()
	serializer_class = StudentUpdateSerializer
	http_method = ['get', 'put']

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
			user_obj = StudentAdmission.objects.get(student_id=pk)
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
		'id':user_obj.id,
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
		user_detail=UserDetail.objects.get(user_id=user.id)
		student=user_obj.student
		# userd=UserGetSerializer(user).data
		# address_detail=AddressSerializer(address).data
		# phone_detail=PhoneSerializer(phone).data
		# fatherd=FatherSerializer(father).data
		# motherd=MotherSerializer(mother).data
		# user_detaild=UserDetailSerializer(user_detail).data

		serializer=StudentUpdateSerializer(data=request.data)

		if serializer.is_valid():
			data=serializer.data
			
			user_obj.batch=data['batch']
		
			student.registration_no=data['registration_no']
			
			user_obj.description=data['description']

			user_obj.course_id=data['course']
			

			address.province=data['address_detail']['province']
			address.city=data['address_detail']['city']
			address.district=data['address_detail']['district']
			address.address=data['address_detail']['address']

			phone.number=data['phone_detail']['number']
			phone.type=data['phone_detail']['type']

			user_detail.blood_group=data['user_detail']['blood_group']
			user_detail.nationality=data['user_detail']['nationality']
			user_detail.mother_tongue=data['user_detail']['mother_tongue']
			user_detail.religion=data['user_detail']['religion']
			user_detail.citiizenship_no=data['user_detail']['citizenship_no']
			
			father.name=data['father']['name']
			father.mobile=data['father']['mobile']
			father.job=data['father']['job']
			father.citizenship_no=data['father']['citizenship_no']
		
			mother.name=data['mother']['name']
			mother.mobile=data['mother']['mobile']
			mother.job=data['mother']['job']
			mother.citizenship_no=data['mother']['citizenship_no']

			

			


			address.save()
			user_detail.save()
			father.save()
			mother.save()
			phone.save()
			student.save()
			user_obj.save()

			return Response(serializer.data,status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors)







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

				return Response(data,status=status.HTTP_201_CREATED)
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
				return Response(data,status=status.HTTP_201_CREATED)
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
	