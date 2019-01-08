# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework import status,viewsets,serializers
# from .serializers import *
# from .models import *
# from django.core.exceptions import ValidationError

# class SchoolViewset(viewsets.ModelViewSet):
#     queryset=School.objects.all()
#     serializer_class=SchoolSerializer

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             School.objects.update_or_create(name=data['name'])
#             return Response(data)
#         else:
#             raise ValidationError({'Detail':[serializer.errors]})

# class DepartmentViewset(viewsets.ModelViewSet):
#     queryset=Department.objects.all()
#     serializer_class=DepartmentSerializer

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             Department.objects.get_or_create(school=School.objects.get(id=data['school']),name=data['name'],description=data['description'])
#             return Response(data)
#         else:
#             raise ValidationError({'Detail':[serializer.errors]})

                






# class CourseViewSet(viewsets.ModelViewSet):
#     queryset=Course.objects.all()
#     serializer_class=CourseSerializer

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             #e, c=Department.objects.get_or_create(name=data['department'])    
#             obj,created =Course.objects.get_or_create(
#             	name=data['name'],
#                 code=data['code'],
#                 defaults={'description':data['description']}
                
#                 )
#             #syllabus_name=data['syllabus_name'])

#             if not created:
#             	raise ValidationError({
# 	        	    'Detail':['Course Already Exist']
# 	       		    })
#             else:
#                 return Response(data,status=status.HTTP_201_CREATED)
      

#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self,request,pk):
#         try:
#             instance = Course.objects.get(id=pk)
#         except Exception as error:
#             return Response(error)
#         dict={
#             'name':instance.name,
#             'description':instance.description,
#             'code':instance.code,
#             'department':instance.department.name
#         }
#         return Response(dict)

#     def list(self,request):
#         object = self.queryset
#         list=[]

#         for obj in object:
#             dct ={'id':obj.id,
#             'department':'',
#             'name':obj.name,
#             'code':obj.code
#             }
#             list.append(dct)

#         return Response(list)



       
    
# class BatchViewSet(viewsets.ModelViewSet):
#     queryset=Batch.objects.all()
#     serializer_class=BatchSerializer

#     def create(self,request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a,b = Batch.objects.get_or_create(course=Course.objects.get(id=data['course']),name=data['name'],start_date=data['start_date'],end_date=data['end_date'],max_no_of_students=data['max_no_of_students'])
#             if not b:
#                 return Response({'Detail':'Batch already exists'},status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(data=data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

#     def list(self,request):
#         objects=self.queryset
#         output=[]
#         for obj in objects:
#             temp={  
#                     'id':obj.id,
#                     'course':obj.course.name,
#                     'name':obj.name,
#                     'start_date':obj.start_date,
#                     'end_date':obj.end_date,
#                     'max_no_of_students':obj.max_no_of_students
#                     }        
#             output.append(temp)
#         return Response(output)    
    
#     def retrieve(self,request,pk):
#         try:
#             instance=Batch.objects.get(id=pk)
#         except Exception as error:
#             return Response(error)
#         dict={
#             'name':instance.name,
#             'course':instance.course.name,
#             'start_date':instance.start_date,
#             'end_date':instance.end_date,
#             'max_no_of_students':instance.max_no_of_students
#         }
#         return Response(dict)
# class AssignSubjectViewset(viewsets.ModelViewSet):
#     serializer_class=AssignSubjectSerializer
#     queryset=AssignSubject.objects.all()

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a,b=AssignSubject.objects.get_or_create(subject=Subject.objects.get(id=data['subject']),batch=Batch.objects.get(id=data['batch']),course=Course.objects.get(id=data['course']))
#             if not b:
#                 return Response({'Detail':'Already assigned'},status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Deatail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST) 
#     def list(self,request):
#         objects=self.queryset
#         output=[]
#         for obj in objects:
#             temp={'id':obj.id,
#             'batch':obj.batch.name,
#             'course':obj.course.name,
#             'subject':obj.subject.name
#             }           
#             output.append(temp)
#         return Response(output)
#     def update(self,request,pk):
#         a=AssignSubject.objects.get(id=pk)
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a.subject=Subject.objects.get(id=data['subject'])
#             a.batch=Batch.objects.get(id=data['batch'])
#             a.course=Course.objects.get(id=data['course'])
#             a.save()
#             return Response(data)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST) 

#     def delete(self,request,pk):
#         a=AssignSubject.objects.get(id=pk)
#         if a:
#             a.delete()
#             return Response({'Detail':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response('Not Found!',status=status.HTTP_404_NOT_FOUND)
#     def  retrieve(self,requets,pk):
#         a=AssignSubject.objects.get(id=pk)
#         temp={'batch':a.batch.name,
#         'course':a.course.name,
#         'subject':a.subject.name
#         }           
#         return Response(temp)          



# class SubjectAllocationViewset(viewsets.ModelViewSet):
#     serializer_class=SubjectAllocationSerializer
#     queryset=SubjectAllocation.objects.all()

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a,b=SubjectAllocation.objects.get_or_create(teacher=Teacher.objects.get(id=data['teacher']),subject=Subject.objects.get(id=data['subject']),batch=Batch.objects.get(id=data['batch']),course=Course.objects.get(id=data['course']))
#             if not b:
#                 return Response({'Detail':'Already assigned'},status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST) 
#     def list(self,request):
#         objects=self.queryset
#         output=[]
#         for obj in objects:
#             temp={'id':obj.id,
#             'batch':obj.batch.name,
#             'course':obj.course.name,
#             'subject':obj.subject.name,
#             'teacher':obj.teacher.user.first_name+" "+obj.teacher.user.last_name
#             }           
#             output.append(temp)
#         return Response(output)
#     def update(self,request,pk):
#         a=SubjectAllocation.objects.get(id=pk)
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a.subject=Subject.objects.get(id=data['subject'])
#             a.batch=Batch.objects.get(id=data['batch'])
#             a.course=Course.objects.get(id=data['course'])
#             a.teacher=Teacher.objects.get(id=data['teacher'])
#             a.save()
#             return Response(data)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST ) 

#     def delete(self,request,pk):
#         a=SubjectAllocation.objects.get(id=pk)
#         if a:
#             a.delete()
#             return Response('Deleted!',status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response('Not Found!',status=status.HTTP_404_NOT_FOUND)
#     def  retrieve(self,requets,pk):
#         a=SubjectAllocation.objects.get(id=pk)
#         temp={'batch':a.batch.name,
#         'course':a.course.name,
#         'subject':a.subject.name,
#         'teacher':a.teacher.user.first_name+" "+a.teacher.user.last_name
#         }           
#         return Response(temp)   

# class ElectiveSubjectViewset(viewsets.ModelViewSet):
#     serializer_class=ElectiveSubjectSerializer
#     queryset=ElectiveSubject.objects.all()

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a,b=ElectiveSubject.objects.get_or_create(student=Student.objects.get(id=data['student']),subject=Subject.objects.get(id=data['subject']),batch=Batch.objects.get(id=data['batch']),course=Course.objects.get(id=data['course']))
#             if not b:
#                 return Response({'Detail':'Already assigned'},status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST) 
#     def list(self,request):
#         objects=self.queryset
#         output=[]
#         for obj in objects:
#             temp={'id':obj.id,
#             'batch':obj.batch.name,
#             'course':obj.course.name,
#             'subject':obj.subject.name,
#             'student':obj.student.user.first_name+" "+obj.student.user.last_name
#             }           
#             output.append(temp)
#         return Response(output)
#     def update(self,request,pk):
#         a=ElectiveSubject.objects.get(id=pk)
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a.subject=Subject.objects.get(id=data['subject'])
#             a.batch=Batch.objects.get(id=data['batch'])
#             a.course=Course.objects.get(id=data['course'])
#             a.student=Student.objects.get(id=data['teacher'])
#             a.save()
#             return Response(data)
#         else:
#             return Response(serializer.errors) 

#     def delete(self,request,pk):
#         a=ElectiveSubject.objects.get(id=pk)
#         if a:
#             a.delete()
#             return Response({'Success!':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({'Detail':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
#     def  retrieve(self,requets,pk):
#         a=ElectiveSubject.objects.get(id=pk)
#         temp={'batch':a.batch.name,
#         'course':a.course.name,
#         'subject':a.subject.name,
#         'student':a.student.user.first_name+" "+a.student.user.last_name
#         }           
#         return Response(temp)           


# class  ClassTeacherAllocationViewSet(viewsets.ModelViewSet):
#     queryset=ClassTeacherAllocation.objects.all()
#     serializer_class=ClassTeacherAllocationSerializer

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a,b=ClassTeacherAllocation.objects.get_or_create(course=Course.objects.get(id=data['course']),batch=Batch.objects.get(id=data['batch']),class_teacher=Teacher.objects.get(id=data['class_teacher']),section=Section.objects.get(id=data['section']))
#             if not b:
#                 return Response({'Detail':'Already Allocated!'},status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

#     def list(self,request):
#         objects=self.queryset
#         output=[]
#         for obj in objects:
#             temp = {'id':obj.id,
#             'course':obj.course.name,
#             'batch':obj.batch.name,
#             'class_teacher':obj.class_teacher.user.first_name+" "+obj.class_teacher.user.last_name,
#             'section':obj.section._class+" "+obj.section.name
#             }
#             output.append(temp)
#         return Response(output)

#     def update(self,request,pk):
#         try:
#             ct=ClassTeacherAllocation.objects.get(id=pk)
#         except:
#             return Response({'Detail':'ClassTeacher object does not exist '},status=status.HTTP_404_NOT_FOUND)
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             ct.course=Course.objects.get(id=data['course'])
#             ct.batch=Batch.objects.get(id=data['batch'])
#             ct.class_teacher=Teacher.objects.get(id=data['class_teacher'])
#             ct.save()
#             return Response(data,status=status.HTTP_200_OK)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self,request,pk):
#         try:
#             ct=ClassTeacherAllocation.objects.get(id=pk)
#         except:
#             return ('ClassTeacher object does not exist ')
#         temp={'course':ct.course.name,
#         'batch':ct.batch.name,
#         'class_teacher':ct.class_teacher.user.first_name+" "+ct.class_teacher.user.last_name}
#         return Response(temp,status=status.HTTP_200_OK)    




# class ClassViewSet(viewsets.ModelViewSet):
#     queryset = Class.objects.all()
#     serializer_class = ClassSerializer
    
#     def create(self,request):

#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data
#             created,psk = Class.objects.get_or_create(name=data['name'],description=data['description'])
#             if not psk:
#                 raise serializers.ValidationError({
#                     'detail':["Class Already Exist"]
#                     })

#             return Response(data,status=status.HTTP_201_CREATED)

#         else:
#             raise serializers.ValidationError(
#                 {
#                 'Detail':[serializer.errors]
#                 })

#     def list(self,request):
#         objects=Class.objects.all()
#         output=[]
#         for obj in objects:
#             temp={
#                 'id':obj.id,
#                 'name':obj.name,
#                 'description':obj.description
#                     }
#             output.append(temp)
#         return Response(output)   



# """ 
# section apis
# """

# class SectionViewSet(viewsets.ModelViewSet):
#     queryset = Section.objects.all()
#     serializer_class = SectionSerializer

#     def list(self, request):
#         objects = self.queryset
#         output = []
#         for obj in objects:
#             temp = {
#                     'id': obj.id,
#                     'name': obj.name,
#                     '_class': obj._class.name
#             }
#             output.append(temp)
#         return Response(output)

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data
#             created, bv = Section.objects.get_or_create(
#                     _class_id=data['_class'],
#                     name=data['name']
#                 )
#             if not bv:
#                 raise serializers.ValidationError(
#                             {
#                     'Detail': ['Section Already Exist']
#                             })

#             return Response(data)
#         else:
#             raise serializers.ValidationError({
#                     'Detail': [serializer.errors]
#                 })

#     def retrieve(self, request, pk):
#         try:
#             section = Section.objects.get(id=pk)
#         except:
#             return Response('Section does not exist!')
#         temp = {}
#         temp['name'] = section.name
#         temp['_class'] = section._class.name
#         return Response(temp)

#     def update(self, request, pk):
#         try:
#             section = Section.objects.get(id=pk)
#         except:
#             return Response('Section does not exist!')
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data
#             section.name = data['name']
#             section._class = Class.objects.get(id=data['_class'])
#             section.save()
#         return Response(data, status=status.HTTP_200_OK)


# class SectionStudentViewSet(viewsets.ModelViewSet):
#     queryset = SectionStudent.objects.all()
#     serializer_class = SectionStudentSerializer

#     def create(self, request):
#         print("hello")
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data
#             std_id = data['student_id']
#             std = Student.objects.filter(id=std_id)
#             sec_id = data['section_id']
#             sec = Section.objects.filter(id=sec_id)
#             if std and sec:
#                 roll = data['roll_no']
#                 vroll = SectionStudent.objects.filter(roll_no=roll)
#                 if vroll:
#                     raise serializers.ValidationError({
#                                             'Detail': ["Student With This Roll_No Already Exist"]
#                                         })
#                 else:
#                     created, bval = SectionStudent.objects.get_or_create(
#                                             student_id=std[0].id, section_id=sec[0].id,
#                                             defaults={
#                                                 'roll_no': data['roll_no']}

#                                         )
#                     if not bval:
#                         raise serializers.ValidationError({
#                                                     'Detail': ['Student Already Exist']

#                                                 })
#             else:
#                 raise serializers.ValidationError(
#                     {
#                                             'Detail': ['Either Section Or Student Not Exist']
#                     })

#             return Response(data)
#         else:
#             raise serializers.ValidationError({
#                             'Detail': [serializer.errors]
#                         })

#     def list(self, request):
#         objects = self.queryset
#         output = []
#         for obj in objects:
#             temp = {
#                             'id': obj.student.user.id,
#                             'student_first_name': obj.student.user.first_name,
#                             'student_last_name': obj.student.user.last_name,
#                             'section_name': obj.section.name,
#                             'roll_no': obj.roll_no
#             }
#             output.append(temp)

#         return Response(output)


# class TeacherSectionViewSet(viewsets.ModelViewSet):
#     queryset = TeacherSection.objects.all()
#     serializer_class = TeacherSectionSerializer

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data

#             sub = data['subject_id']
#             sub_id = Subject.objects.filter(id=sub)

#             sec = data['section_id']
#             sec_id = Section.objects.filter(id=sec)

#             teacher = data['teacher_id']
#             teacher_id = Teacher.objects.filter(id=teacher)

#             if sub_id and sec_id and teacher_id:
#                 TeacherSection.objects.get_or_create(section_id=sec_id.first().id,
#                                          defaults={
#                                     'subject_id': sub_id.first().id,
#                                                                         'teacher_id': teacher_id.first().id
#                                 })
#                 return Response(data)
#             else:
#                 raise serializers.ValidationError({
#                                     'Detail': ['Either Section Or Teacher Or Subject Not Exist']
#                                 })
#         else:
#             raise serializers.ValidationError({
#                             'Detail': [serializer.errors]
#                         })


# class SectionRoutineViewSet(viewsets.ModelViewSet):
#     queryset = SectionRoutine.objects.all()
#     serializer_class = SectionRoutineSerializer

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data
#             teacher_section_id = data['teacher_section_id']
#             ts_id = TeacherSection.objects.filter(id=teacher_section_id)
#             if ts_id:
#                 SectionRoutine.objects.get_or_create(teacher_section=ts_id[0],
#                                          defaults={
#                                     'day_of_week': data['day_of_week'],
#                                                                         'start_time': data['start_time'],
#                                                                         'end_time': data['end_time']
#                                 })
#                 return Response(data)
#             else:
#                 raise serializers.ValidationError({
#                                     "Detail": ['TeacherSection Id Not Found']
#                                 })
#         else:
#             raise serializers.ValidationError({
#                             "Detail": [serializer.errors]
#                         })

#     def list(self, request):
#         return Response("List IS in under Construction")
#                   