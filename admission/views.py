from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from course.models import Batch,Course
from main.models import User,Address,Phone,UserDetail,Parent,GENDER
from student.models import Student
from .models import StudentAdmission
from .serializers import StudentAdmissionSerializer,UserSerializer,AddressSerializer,PhoneSerializer,UserDetailSerializer
from main.helpers.parser import NestedMultipartParser
from main.helpers.tuple import get_choice_string
from Section.models import Section,SectionStudent
from guardian.models import Guardian,GuardianStudent
from transport.models import TransportAllocation,Route
class StudentAdmissionViewSet(viewsets.ModelViewSet):
	queryset = StudentAdmission.objects.all()
	serializer_class = StudentAdmissionSerializer
	#parser_classes = (NestedMultipartParser,)
	def list(self,request):
		output=[]
		for obj in self.queryset:
			temp={'id':obj.id}
			output.append(temp)
		return Response(output)	

	def create(self,request):
		print(request.data)
		serializer = self.get_serializer(data={**request.data,**request.FILES})
		if serializer.is_valid():
			data = serializer.data
			ud = data['user']


			user,b = User.objects.get_or_create(
				email = ud['email'],
				defaults={'username' : ud['email'],
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
		
			if data['father']:
				Parent.objects.get_or_create(content_type=c,object_id=user.id,
				defaults={			
				'name':data['father']['name'],
				'mobile':data['father']['mobile'],
				'job':data['father']['job'],
				'citizenship_no':data['father']['citizenship_no']
					},
				type='Father'	
				)
			if data['mother']:
				Parent.objects.get_or_create(content_type=c,object_id=user.id,
				defaults={			
					'name':data['mother']['name'],
					'mobile':data['mother']['mobile'],
					'job':data['mother']['job'],
					'citizenship_no':data['mother']['citizenship_no']
					},
					type='Mother'
				)
			if data['father'] and data['mother']:
				Parent.objects.get_or_create(content_type=c,object_id=user.id,defaults={'name':data['father']['name'],'mobile':data['father']['mobile'],'job':data['father']['job'],'citizenship_no':data['father']['citizenship_no']},type='Father')
				Parent.objects.get_or_create(content_type=c,object_id=user.id,defaults={'name':data['mother']['name'],'mobile':data['mother']['mobile'],'job':data['mother']['job'],'citizenship_no':data['mother']['citizenship_no']},type='Mother')

			# 	Father.objects.get_or_create(defaults={'name':Parent.name,'mobile':Parent.mobile,'job':Parent.job,'citizenship':Parent.citizenship})
			# if data['parent_detail']['type']=='Mother':
			# 	Mother.objects.get_or_create(defaults={'name':Parent.name,'mobile':Parent.mobile,'job':Parent.job,'citizenship':Parent.citizenship})
			guser=User.objects.get_or_create(first_name=data['guardian']['guser']['first_name'],last_name=data['guardian']['guser']['last_name'],email=data['guardian']['guser']['email'],gender=data['guardian']['guser']['gender'],type=data['guardian']['guser']['type'])[0]
			guardian,b=Guardian.objects.get_or_create(user=guser,type=data['guardian']['guardian_type'])
			gaddress=Address.objects.get_or_create(content_type=ContentType.objects.get_for_model(guser),object_id=guser.id,defaults=AddressSerializer(data['guardian']['address_detail']).data)[0]
			gphone=Phone.objects.get_or_create(content_type=ContentType.objects.get_for_model(guser),object_id=guser.id,defaults=PhoneSerializer(data['guardian']['phone_detail']).data)[0]
			
			section,val=Section.objects.get_or_create(_class_id=data['section']['_class_id'],name=data['section']['name'])

			student,bval = Student.objects.get_or_create(user_id=user.id,registration_no=data['registration_no'])

			if guardian:
				GuardianStudent.objects.get_or_create(student_id=student.id,guardian_id=guardian.id)
			if section:
				SectionStudent.objects.get_or_create(section_id=section.id,student_id=student.id,roll_no=student.registration_no)	
			stdadm,vals=StudentAdmission.objects.get_or_create(student_id=student.id,
												   defaults={   
												   'batch':data['batch'],
												   'course_id':data['course'],
												   'description':data['description'],
												   #'image':data['image
												   }
												   )
												   
			if stdadm:
				TransportAllocation.objects.get_or_create(route=Route.objects.get(id=data['transport']['route']),batch=Batch.objects.get(id=stdadm.batch),course=stdadm.course,student=student,_class=section._class,section=section)



				
			return Response(data,status=status.HTTP_201_CREATED)

		else:
			raise serializers.ValidationError({
					'detail':serializer.errors
					})

