from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import *
from .serializers import *
import datetime
from datetime import date,time

class TermViewset(viewsets.ModelViewSet):
    queryset=Term.objects.all()
    serializer_class=TermSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Term.objects.get_or_create(name=data['name'],start_date=data['start_date'],end_date=data['end_date'],batch=Batch.objects.get(id=data['batch']))
            if not b:
                return Response({'Term':'Already Created!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Error!':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'name':obj.name,
            'start_date':obj.start_date,
            'end_date':obj.end_date,
            'batch':obj.batch.name
            }
            output.append(temp)
        return Response(output)

    def retrieve(self,request,pk):
        try:
            term=Term.objects.get(id=pk)
        except:
            return Response({'Error':'Exam Term not found!'},status=status.HTTP_404_NOT_FOUND)
        temp={'name':term.name,
        'batch':term.batch.name,
        'batch_id':term.batch.id,
        'start_date':term.start_date,
        'end_date':term.end_date
        }
        return Response(temp)
    def update(self,request,pk):
        try:
            trm=Term.objects.get(id=pk)
        except:
            return Response({'Error':'Exam Term not found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data 
            trm.name=data['name']
            trm.batch=Batch.objects.get(id=data['batch'])
            trm.start_date=data['start_date']
            trm.end_date=data['end_date']
            trm.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            trm=Term.objects.get(id=pk)
        except:
            return Response({'Error':'Exam Term not found!'},status=status.HTTP_404_NOT_FOUND)
        trm.delete()
        return Response({'Success!':'Deleted'},status=status.HTTP_204_NO_CONTENT)

class ScheduleViewset(viewsets.ModelViewSet):
    serializer_class=ScheduleSerializer
    queryset=Schedule.objects.all()

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Schedule.objects.get_or_create(subject=Subject.objects.get(id=data['subject']),term=Term.objects.get(id=data['term']),start_time=data['start_time'],end_time=data['end_time'],date=data['date'])
            if not b:
                return Response({'Schedule':'Already Created'},status=status.HTTP_400_BAD_REQUEST)
            else:
                 return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'date':obj.date,
            'day':obj.date.strftime("%A"),
            'subject':obj.subject.name,
            'term':obj.term.name,
            'start_time':obj.start_time,
            'end_time':obj.end_time,
            'batch':obj.term.batch.name
            }
            output.append(temp)
        return Response(output)
    def retrieve(self,request,pk):
        try:
            s=Schedule.objects.get(id=pk)
        except:
            return Response({'Detail':'Schedule not found!'},status=status.HTTP_404_NOT_FOUND)
        temp={'subject':s.subject.name,
        'term':s.term.name,
        'start_time':s.start_time,
        'end_time':s.end_time,
        'date':s.date,
        'day':s.date.strftime("%A"),
        'batch':s.term.batch.name
        }
        return Response(temp)

    def update(self,request,pk):
        try:
            s=Schedule.objects.get(id=pk)
        except:
            return Response({'Detail':'Schedule not found'},status=status.HTTP_404_NOT_FOUND)

        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            s.term=Term.objects.get(id=data['term'])
            s.start_time=data['start_time']
            s.end_time=data['end_time']
            s.date=data['date']
            s.subject=Subject.objects.get(id=data['subject'])
            s.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            s=Schedule.objects.get(id=pk)
        except:
            return Response({'Detail':'Schedule not found'},status=status.HTTP_404_NOT_FOUND)
        s.delete()
        return Response({'Success!':'Deleted'},status=status.HTTP_204_NO_CONTENT)         


class AddMarksViewSet(viewsets.ModelViewSet):
    queryset=Marks.objects.all()
    serializer_class=MarksSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Marks.objects.get_or_create(_class=Class.objects.get(id=data['_class']),section=Section.objects.get(id=data['section']),subject=Subject.objects.get(id=data['subject']),exam=Term.objects.get(id=data['exam']),theory_fm=data['theory_fm'],theory_pm=data['theory_pm'],practical_fm=data['practical_fm'],practical_pm=data['practical_pm'],full_marks=data['theory_fm']+data['practical_fm'],pass_marks=data['theory_pm']+data['practical_pm'])
            if not b:
                return Response({'Detail':'Marks alredy added!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:

            temp={'id':obj.id,
            'class':obj._class.name,
            'section':obj.section.name,
            'subject':obj.subject.name,
            'exam':obj.exam.name,
            'theory_fm':obj.theory_fm,
            'theory_pm':obj.theory_pm,
            'practical_fm':obj.practical_fm,
            'practical_pm':obj.practical_pm,
            'full_marks':obj.full_marks,
            'pass_marks':obj.pass_marks
            }
            output.append(temp)
        return Response(output)    
    def retrieve(self,request,pk):
        try:
            obj=Marks.objects.get(id=pk)
        except:
            return Response({'Detail':'Not found!'},status=status.HTTP_404_NOT_FOUND)
        temp={
            'class':obj._class.name,
            'section':obj.section.name,
            'subject':obj.subject.name,
            'exam':obj.exam.name,
            'theory_fm':obj.theory_fm,
            'theory_pm':obj.theory_pm,
            'practical_fm':obj.practical_fm,
            'practical_pm':obj.practical_pm,
            'full_marks':obj.full_marks,
            'pass_marks':obj.pass_marks
            }
        return Response(temp)
    def update(self,request,pk):
        try:
            obj=Marks.objects.get(id=pk)
        except:
            return Response({'Detail':'Not found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            obj._class=Class.objects.get(id=data['_class'])
            obj.section=Section.objects.get(id=data['section'])
            obj.subject=Subject.objects.get(id=data['subject'])
            obj.exam=Term.objects.get(id=data['exam'])
            obj.theory_fm=data['theory_fm']
            obj.theory_pm=data['theory_pm']
            obj.practical_fm=data['practical_fm']
            obj.practical_pm=data['practical_pm']
            obj.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)   

class StudentmarksViewSet(viewsets.ModelViewSet):
    queryset=Studentmarks.objects.all()
    serializer_class=StudentmarksSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Studentmarks.objects.get_or_create(student=Student.objects.get(id=data['student']),marks=Marks.objects.get(id=data['marks']),obtained_theory_marks=data['obtained_theory_marks'],obtained_practical_marks=data['obtained_practical_marks'])
            if not b:
                return Response({'Detail':'Stduent_Marks already added!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'student':obj.student.user.first_name+" "+obj.student.user.last_name,
            'marks':{"_class":obj.marks._class.name,
                    "section":obj.marks.section.name,
                    "subject":obj.marks.subject.name,
                    "exam":obj.marks.exam.name,
                    "theory_fm":obj.marks.theory_fm,
                    "theory_pm":obj.marks.theory_pm,
                    "practical_fm":obj.marks.practical_fm,
                    "practical_pm":obj.marks.practical_pm},
            'obtained_theory_marks':obj.obtained_theory_marks,
            'obtained_practical_marks':obj.obtained_practical_marks
            }
            if obj.obtained_theory_marks<obj.marks.theory_pm and obj.obtained_practical_marks>=obj.marks.practical_pm:
                status='Failed in theory'
            elif obj.obtained_practical_marks<obj.marks.practical_pm and obj.obtained_theory_marks>=obj.marks.theory_pm:
                status='Failed in practical'
            elif obj.obtained_practical_marks<obj.marks.practical_pm and obj.obtained_theory_marks<obj.marks.theory_pm:
                status='Failed! in theory and in practical'
            elif obj.obtained_practical_marks>=obj.marks.practical_pm and obj.obtained_theory_marks>=obj.marks.theory_pm:
                status='Passed!'
            elif obj.obtained_practical_marks>obj.marks.practical_fm or obj.obtained_theory_marks>obj.marks.theory_fm:
                status='Error!:The obtained marks in theory or practical is more than full marks!'
            sts=status
            temp['total_obtained_marks']=obj.obtained_theory_marks+obj.obtained_practical_marks
            temp['status']=sts

            output.append(temp)
        return Response(output)


    def retrieve(self,request,pk):
        try:
            obj=Studentmarks.objects.get(id=pk)
        except:
            return Response({'Detail':'Not found student marks object!'},status=status.HTTP_404_NOT_FOUND)
        temp={
            'student':obj.student.user.first_name+" "+obj.student.user.last_name,
            'marks':{"_class":obj.marks._class.name,
                    "section":obj.marks.section.name,
                    "subject":obj.marks.subject.name,
                    "exam":obj.marks.exam.name,
                    "theory_fm":obj.marks.theory_fm,
                    "theory_pm":obj.marks.theory_pm,
                    "practical_fm":obj.marks.practical_fm,
                    "practical_pm":obj.marks.practical_pm},
            'obtained_theory_marks':obj.obtained_theory_marks,
            'obtained_practical_marks':obj.obtained_practical_marks
            }
        if obj.obtained_theory_marks<obj.marks.theory_pm and obj.obtained_practical_marks>=obj.marks.practical_pm:
            stat='Failed in theory'
        elif obj.obtained_practical_marks<obj.marks.practical_pm and obj.obtained_theory_marks>=obj.marks.theory_pm:
            stat='Failed in practical'
        elif obj.obtained_practical_marks<obj.marks.practical_pm and obj.obtained_theory_marks<obj.marks.theory_pm:
            stat='Failed! in theory and in practical'
        elif obj.obtained_practical_marks>=obj.marks.practical_pm and obj.obtained_theory_marks>=obj.marks.theory_pm:
            stat='Passed!'
        elif obj.obtained_practical_marks>obj.marks.practical_fm or obj.obtained_theory_marks>obj.marks.theory_fm:
            stat='Error!:The obtained marks in theory or practical is more than full marks!'
        sts=stat
        temp['total_obtained_marks']=obj.obtained_theory_marks+obj.obtained_practical_marks
        temp['status']=sts
        return Response(temp)
    def update(self,request,pk):
        try:
            obj=Studentmarks.objects.get(id=pk)
        except:
            return Response({'Detail':'Not found student marks object!'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            obj.student=Student.objects.get(id=data['student'])
            obj.marks=Marks.objects.get(id=data['marks'])
            obj.obtained_theory_marks=data['obtained_theory_marks']
            obj.obtained_practical_marks=data['obtained_practical_marks']
            obj.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)           

