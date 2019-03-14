from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework import serializers

from .serializers import *

from .models import *
from academic.models import Class,Course
from student.models import *



class SubjectViewSet(viewsets.ModelViewSet):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer
    
	def create(self,request):
		serializer = SubjectSerializer(data=request.data)
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
			return Response(serializer.data,status=status.HTTP_201_CREATED)

		else:
			raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})

	def list(self,request):
		objects = Subject.objects.all()
		output=[]
		for obj in objects:
			temp={'id':obj.id,
			'name':obj.name,
			'code':obj.code,
			'description':obj.description
			}
			output.append(temp)
		return Response(output)	

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
	
		subject.delete()
		return Response({'Success!':'Deleted Subject instance succesfully'},status=status.HTTP_204_NO_CONTENT)


class ClassSubjectViewSet(viewsets.ModelViewSet):
    queryset = AssignSubject.objects.all()  
    serializer_class = ClassSubjectSerializer

    def list(self,request):
        objects = AssignSubject.objects.filter(_class_id=request.GET['class'])
        data = ClassSubjectSerializer(objects,many=True).data
        return Response(data)

class ExamTermViewset(viewsets.ModelViewSet):
    queryset = ExamTerm.objects.all()
    serializer_class = ExamTermSerializer

    def list(self,request):
        _queryset = self.get_queryset()
        terms = []
        for obj in _queryset:
            temp = {
               'id':obj.id,
               'name':obj.name,
               'start_date':obj.start_date,
               'end_date':obj.end_date,
               '_class':obj._class.name

                }
            
            terms.append(temp)
        return Response(terms,status=status.HTTP_200_OK)

    def retrieve(self,request,pk):
        obj = self.get_object()
        term = {
            'id':obj.id,
            'name':obj.name,
            'start_date':obj.start_date,
            'end_date':obj.end_date,
            '_class':obj._class.name
        }
        return Response(term, status=status.HTTP_200_OK)


class ExamScheduleViewset(viewsets.ModelViewSet):
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleSerializer

    def create(self,request):
        serializer = ExamScheduleSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            try:
                e = ExamTerm.objects.get(id=data['exam'])
            except:
                return Response("Exam With This Id Not Exist",status=status.HTTP_400_BAD_REQUEST)

            if e:
                obj,created = ExamSchedule.objects.get_or_create(subject_id=data['subject'],
                                                                exam_id=data['exam'],
                                                                defaults={
                                                                    'date':data['date'],
                                                                    'start_time':data['start_time'],
                                                                    'end_time':data['end_time'],

                                                                })
                if not created:
                    raise serializers.ValidationError({
                        'Detail':['Already Scheduled This exam']
                    })
                return Response(data,status=status.HTTP_201_CREATED)
        raise serializers.ValidationError({
            "Detail":[serializer.errors]
        })
    def list(self,request):
        queryset = self.get_queryset()
        output = []
        for obj in queryset:
            temp = {
                'id':obj.id,
                'subject':obj.subject.name,
                'date':obj.date,
                'start_time':obj.start_time,
                'end_time':obj.end_time
            }
            output.append(temp)

        return Response(output,status=status.HTTP_200_OK)

    def get_object(self,pk):
        try:
            return ExamSchedule.objects.get(id=pk)
        except:
            return Response("This Objects Not Exist",status=status.HTTP_404_NOT_FOUND)

    def retrieve(self,request,pk):
        obj = self.get_object(pk)
        output = {
                'id':obj.id,
                'subject':obj.subject.name,
                'date':obj.date,
                'start_time':obj.start_time,
                'end_time':obj.end_time
            }
        return Response(output,status=status.HTTP_200_OK)

    def update(self,request,pk):
        obj = self.get_object(pk)
        serializer = ExamScheduleSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            obj.subject_id = data.get('subject',obj.subject)
            obj.date = data.get('date',obj.date)
            obj.start_time = data.get('start_time',obj.start_time)
            obj.end_time = data.get('end_time',obj.end_time)
            obj.save()
            return Response(data,status=status.HTTP_200_OK)
        raise serializers.ValidationError({
            "Detail":[serializer.errors]
        })

class MarksEntryGetViewSet(viewsets.ModelViewSet):
    queryset = MarksEntryDetail.objects.all()
    serializer_class = MarksEntrySerializer

    def list(self,request):
        objects = MarksEntryDetail.objects.filter(marks_entry__subject_id=request.GET['subject'],
                                                marks_entry__section_id=request.GET['section'],
                                                marks_entry__section___class_id=request.GET['class'],
                                                marks_entry__exam_id = request.GET['exam'])

        std_objects = StudentEnroll.objects.filter(_class_id=request.GET['class'],
                                                    section_id=request.GET['section'])
        
        if not objects:
            data= MarksEntryGetSerializer(std_objects,many=True).data
            return Response(data)

        data = MarksEntryGetSerializer(objects,many=True).data
        return Response(data)


class MarksEntryViewSet(viewsets.ModelViewSet):
    queryset = MarksEntry.objects.all()
    serializer_class = MarksEntrySerializer()

    def create(self,request):
        serializer = MarksEntrySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            std_data = data['student_data']
            marks_type = data['marks_type']
            print(marks_type)
            try:
                ExamTerm.objects.get(id=data['exam'])
            except:
                raise serializers.ValidationError({
                    "Detail":['Exam With This Id Not Exist']
                })
            me,created = MarksEntry.objects.update_or_create(section_id=data['section'],
                                        exam_id=data['exam'],
                                        subject_id=data['subject'],
                                        defaults={**marks_type})
            for dct in std_data:
                obj,created = MarksEntryDetail.objects.update_or_create(student_id=dct['id'],
                                                                    marks_entry_id=me.id,
                                                                defaults={
                                                                    'discipline':data['discipline'],
                                                                    'theory':dct['theory'],
                                                                    'practical':dct['practical'],
                                                                    
                                                      }) 
            return Response(data,status=status.HTTP_201_CREATED)
        raise serializers.ValidationError({
            "Detail":[serializer.errors]
        })



class PrepareResultViewSet(viewsets.ModelViewSet):
    queryset = MarksEntry.objects.all()
    serializer_class = ResultPrepareViewSet

    def create(self,request):
        data = request.data
        print(data)
    
        for objs in data['result_preparation']:
            obj = MarksEntryDetail.objects.filter(student_id=objs['student_id'])
        
            for o in obj:
                sub_id = o.marks_entry.subject.id
                if sub_id == data['subject']:
                    # print("Student_id",o.student.user.first_name)
                    o.discipline = objs['discipline']
                    o.save()
                

        
        return Response(data,status=status.HTTP_201_CREATED)

  

    def list(self,request):
        searchword=request.GET
        section_id = searchword.get('section')
        subject_id = searchword.get('subject')
        exam_id = searchword.get('exam')
        objects = MarksEntryDetail.objects.filter(marks_entry__section_id=
                                                section_id,
                                                marks_entry__subject_id=
                                                subject_id,
                                                marks_entry__exam_id=
                                                exam_id,)
        output = ResultPrepareViewSet(objects,many=True).data
        return Response(output,status=status.HTTP_200_OK)


class ViewResultViewSet(viewsets.ModelViewSet):
    queryset = MarksEntryDetail.objects.all()
    serializer_class = ResultPrepareViewSet

    def retrieve(self,request,pk):
        student_id = pk
        output = []
        objects= MarksEntryDetail.objects.filter(student_id=pk)
        std = objects[0]

        mydict = {
            'name':std.student.user.first_name +' '+ std.student.user.last_name,
        }

        subjects = []
        total_mark = 0
        if request.GET['marksheet']=='marksheet':
            for obj in objects:
                temp = {
                    'subject':obj.marks_entry.subject.name,
                    'theory':obj.theory,
                    'practical':obj.practical,
                    'pass_mark':obj.marks_entry.pass_marks,
                    'full_mark':obj.marks_entry.full_marks,
                    'total_in_sub':obj.theory + obj.practical,
                }
                total_mark += obj.theory + obj.practical
                subjects.append(temp)
           
            
            mydict['markdetail'] = subjects
            mydict['total_mark'] = total_mark
           
            return Response(mydict,status=status.HTTP_200_OK)
        elif request.GET['marksheet']=='gpa':
            return Response("Grade is making")
