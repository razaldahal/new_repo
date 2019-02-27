from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework import serializers

from .serializers import *

from .models import *
from academic.models import Class,Course



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
		objects=self.queryset
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


class ExamTermViewset(viewsets.ViewSet):
    queryset = ExamTerm.objects.all()
    serializer_class = ExamTermSerializer

    def get_object(self,pk):
        try:
            return ExamTerm.objects.get(id=pk)
        except:
            raise serializers.ValidationError({
                "Detail":["Exams With this id not Exist"]
            })

    def create(self,request):
        serializer = ExamTermSerializer(data=request.data)
       # serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            try:
                c_id = Course.objects.get(id=data['course'])
            except:
                raise serializers.ValidationError({
                    "Detail":['Course With This Id Dont Exist']
                })
            try:
                _c_id = Class.objects.get(id=data['_class'])
            except:
                raise serializers.ValidationError({
                    "Detail":['Class With This Id Dont Exist']
                })
            # val = seria
            
            if c_id and _c_id:
                _exm,c = ExamTerm.objects.get_or_create(name = data['name'],
                                                     _class_id= data['_class'],
                                                    defaults = {
                                                        'start_date':data['start_date'],
                                                        'end_date':data['end_date'],
                                                        'course_id':data['course'],
                                                        
                                                    })
                if not c:
                    raise serializers.ValidationError({
                    "Detail":['Exam With This name Already Exist']
                                                })
                return Response(data , status=status.HTTP_201_CREATED)
                                        
        else:
            raise serializers.ValidationError({
                "Detail":[serializer.errors]
            })
    def list(self,request):
        _queryset = self.queryset
        terms = []
        for obj in _queryset:
            temp = {
               'id':obj.id,
               'name':obj.name,
               'start_date':obj.start_date,
               'end_date':obj.end_date,
               'course':obj.course.name,
               '_class':obj._class.name

                }
            
            terms.append(temp)
        return Response(terms,status=status.HTTP_200_OK)

    def retrieve(self,request,pk):
        obj = self.get_object(pk)
        term = {
            'id':obj.id,
            'name':obj.name,
            'start_date':obj.start_date,
            'end_date':obj.end_date,
            'course':obj.course.name,
            '_class':obj._class.name
        }
        return Response(term, status=status.HTTP_200_OK)

    def update(self,request,pk):
        instance = self.get_object(pk)
        serializer = ExamUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
           # print(data)
            serializer.partial_update(instance,data)
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExamScheduleViewset(viewsets.ViewSet):
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
        queryset = self.queryset
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


class MarksEntryViewSet(viewsets.ViewSet):
    queryset = MarksEntry.objects.all()

    def create(self,request):
        serializer = MarksEntrySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            std_data = data['student_data']
            marks_type = data['marks_type']
            try:
                ExamTerm.objects.get(id=data['exam'])
            except:
                raise serializers.ValidationError({
                    "Detail":['Exam With This Id Not Exist']
                })
            me,created = MarksEntry.objects.get_or_create(section_id=data['section'],
                                        exam_id=data['exam'],
                                        subject_id=data['subject'],)
            if not created:
                raise serializers.ValidationError({
                    "Detail":['Subject Should Unique']
                })
            print(me.id)
            for dct in std_data:
                obj,created = MarksEntryDetail.objects.get_or_create(student_id=dct['id'],
                                                                    marks_entry_id=me.id,
                                                                defaults={
                                                                    'discipline':dct['discipline'],
                                                                    'theory':dct['theory'],
                                                                    'practical':dct['practical'],
                                                                    'full_marks':marks_type['full_marks'],
                                                                    'full_marks_th':marks_type['full_marks_th'],
                                                                    'full_marks_pr':marks_type['full_marks_pr'],
                                                                    'pass_marks':marks_type['pass_marks'],
                                                                    'pass_marks_th':marks_type['pass_marks_th'],
                                                                    'pass_marks_pr':marks_type['pass_marks_pr']
                                                      }) 
                if not created:
                    raise serializers.ValidationError({
                        "Detail":["Student with this id Already Recorded"]
                    })
                bol = True
    
            if bol:
                return Response(data,status=status.HTTP_201_CREATED)
        raise serializers.ValidationError({
            "Detail":[serializer.errors]
        })

class ViewResultViewSet(viewsets.ViewSet):
    queryset = MarksEntryDetail.objects.all()

   
    def retrieve(self,request,pk):
        output = []
        objects= MarksEntryDetail.objects.filter(student_id=pk)
        std = objects[0]

        mydict = {
            'name':std.student.user.first_name +' '+ std.student.user.last_name,
        }

        subjects = []
        total_mark = 0
        for obj in objects:
            temp = {
                'subject':obj.marks_entry.subject.name,
                'theory':obj.theory,
                'practical':obj.practical,
                'pass_mark':obj.pass_marks,
                'full_mark':obj.full_marks,
                'total_in_sub':obj.theory + obj.practical,
            }
            total = obj.theory + obj.practical
            total_mark =total_mark + total
            subjects.append(temp)
       
        
        mydict['markdetail'] = subjects
        mydict['total_mark'] = total_mark
       
        return Response(mydict,status=status.HTTP_200_OK)

class PrepareResultViewSet(viewsets.ViewSet):
    queryset = MarksEntry.objects.all()

    def get_filter(self,section_id,subject_id,exam_id):
        return MarksEntryDetail.objects.filter(marks_entry__section_id=
                                                section_id,
                                                marks_entry__subject_id=
                                                subject_id,
                                                marks_entry__exam_id=
                                                exam_id,)

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
        med = self.get_filter(section_id,subject_id,exam_id)
        output = []
        for marks in med:
            temp = {
                'student_id':marks.student.id,
                'student_name':marks.student.user.first_name + ' ' + marks.student.user.last_name,
                'theory':marks.theory ,
                'practical':marks.practical,
                'total':marks.theory + marks.practical,
                'discipline':marks.discipline,
               
            }
            output.append(temp)
        return Response(output,status=status.HTTP_200_OK)



# output = {}
# med = MarksEntryDetail.objects.filter(marks_entry__section_id=<input>, ....)
# for m in med:
#     student_id = m.student.id

#     tmp = {
#         'student_name': m.student.first_name,
#         'theory' : m.theory
#     }
#     if student_id not in output:
#         output[student_id] = tmp
#     else:
#         tmp1 = output[student_id]
#         tmp1['theory'] += m.theory
#         output[student_id] = tmp1
