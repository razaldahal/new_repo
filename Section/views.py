from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from student.models import Student,SectionStudent
from teacher.models import Teacher,Subject
from .models import Section,TeacherSection,SectionRoutine
from .serializers import SectionSerializer ,SectionStudentSerializer,TeacherSectionSerializer,SectionRoutineSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def list(self,request):
    	objects = self.queryset
    	output = []
    	for obj in objects:
    		temp={
    		'id':obj.id,
    		'name':obj.name
    		}
    		output.append(temp)
    	return Response(output)

    def create(self,request):
    	serializer=self.get_serializer(data=request.data)
    	if serializer.is_valid():
    		data=serializer.data
    		created,bv=Section.objects.get_or_create(
            	_class_id=data['_class'],
            	name=data['name']
            	)
    		if not bv:
    			raise serializers.ValidationError(
    				{
    				'Detail':['Section Already Exist']
    				})

    		return Response(data)
    	else:
    		raise serializers.ValidationError({
    			'Detail':[serializer.errors]
    			})
	

class SectionStudentViewSet(viewsets.ModelViewSet):
	queryset = SectionStudent.objects.all()
	serializer_class = SectionStudentSerializer

	def create(self,request):
		print("hello")
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			std_id = data['student_id']
			std = Student.objects.filter(id=std_id)
			sec_id = data['section_id']
			sec = Section.objects.filter(id=sec_id)
			if std and sec:
				roll= data['roll_no']
				vroll = SectionStudent.objects.filter(roll_no=roll)
				if vroll:
					raise serializers.ValidationError({
						'Detail':["Student With This Roll_No Already Exist"]
						})
				else:
					created,bval=SectionStudent.objects.get_or_create(
							student_id=std[0].id,section_id=sec[0].id,
							defaults={'roll_no':data['roll_no']}

							)
					if not bval:
						raise serializers.ValidationError({
								'Detail':['Student Already Exist']
				
								})
			else:
				raise serializers.ValidationError(
					{
					'Detail':['Either Section Or Student Not Exist']
					})

			return Response(data)
		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})


	def list(self,request):
		objects = self.queryset
		output = []
		for obj in objects:
			temp ={
			'student_first_name':obj.student.user.first_name,
			'student_last_name':obj.student.user.last_name,
			'section_name':obj.section.name,
			'roll_no' : obj.roll_no
			}
			output.append(temp)

		return Response(output)

class TeacherSectionViewSet(viewsets.ModelViewSet):
	queryset = TeacherSection.objects.all()
	serializer_class = TeacherSectionSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data

			sub = data['subject_id']
			sub_id = Subject.objects.filter(id=sub)

			sec = data['section_id']
			sec_id = Section.objects.filter(id=sec)

			teacher  = data['teacher_id']
			teacher_id = Teacher.objects.filter(id=teacher)

			if sub_id and sec_id and teacher_id:
				TeacherSection.objects.get_or_create(section_id = sec_id.first().id,
													defaults={
													'subject_id':sub_id.first().id,
													'teacher_id':teacher_id.first().id
													})
				return Response(data)
			else:
				raise serializers.ValidationError({
					'Detail':['Either Section Or Teacher Or Subject Not Exist']
					})
		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})


class SectionRoutineViewSet(viewsets.ModelViewSet):
	queryset = SectionRoutine.objects.all()
	serializer_class = SectionRoutineSerializer

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			teacher_section_id = data['teacher_section_id']
			ts_id = TeacherSection.objects.filter(id=teacher_section_id)
			if ts_id:
				SectionRoutine.objects.get_or_create(teacher_section=ts_id[0],
													defaults={
													'day_of_week':data['day_of_week'],
													'start_time':data['start_time'],
													'end_time':data['end_time']
													})
				return Response(data)
			else:
				raise serializers.ValidationError({
					"Detail":['TeacherSection Id Not Found']
					})
		else:
			raise serializers.ValidationError({
				"Detail":[serializer.errors]
				})

	def list(self,request):
		return Response("List IS in under Construction")

		

		