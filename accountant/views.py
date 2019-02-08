from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.response import Response
# Create your views here.
from datetime import datetime,date


import calendar
from teacher.models import Teacher
from Section.models import SectionStudent,Section
class AccountantViewset(viewsets.ModelViewSet):
    queryset=Accountant.objects.all()
    serializer_class=AccountantSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            user=data['user']
            esp_idd=data['esp_id']
            try:
                x = User.objects.get(email=user['email'],type=5)
                y = Accountant.objects.get_or_create(user=x,esp_id=esp_idd)
        
            except:
                a,b = User.objects.get_or_create(email=user['email'],defaults={'first_name':user['first_name'],'last_name':user['last_name'],'username':user['email'],'gender':user['gender'],'type':5}) 
    
                if  not b:
                    raise serializers.ValidationError(
					    {
					    'Detail':['Enter Unique Email']
					    })   
                else:
                    c,d = Accountant.objects.get_or_create(user=a,esp_id=esp_idd)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError({
				'Detail':[serializer.errors]
				})
                
    def list(self,request):

        objects = self.queryset
        output = []
        for obj in objects:
            temp={'email':obj.user.email,
            'name':obj.user.first_name+' '+obj.user.last_name,
            'type':obj.user.type,
            'esp_id':obj.esp_id}
            output.append(temp) 
        return Response(output)
                







class PaymentTypeViewSet(viewsets.ModelViewSet):
    serializer_class=PaymentTypeSerializer
    queryset=PaymentType.objects.all()
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            pt,c=PaymentType.objects.update_or_create(name=data['name'],_class=Class.objects.get(id=data['_class']),rate=data['rate'])
            if not c:
                return Response({'Error':'PaymentType already exists'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk):
        try:
            obj=PaymentType.objects.get(_class_id=pk)
        except:
            return Response({'Not found':'Payment Types not registered for given class id'},status=status.HTTP_404_NOT_FOUND)
        temp={'id':obj.id,
        'name':obj.name,
        'rate':obj.rate,
        'class':obj._class.name,
        'id':obj._class.id
        }
        return Response(temp)                   
    def update(self,request,pk):
        try:
            obj=PaymentType.objects.get(_class_id=pk)
        except:
            return Response({'Not found':'Payment Types not registered for given class id'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            obj.name=data['name']
            obj._class=Class.objects.get(id=data['class'])
            obj.rate=data['rate']
            obj.save()
        return Response(data,status=status.HTTP_200_OK)

class PaymentsViewSet(viewsets.ModelViewSet):
    queryset=Payments.objects.all()
    serializer_class=PaymentsSerializer
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            pb=data['paid_by']
            pf=data['paid_for']
            x=Student.objects.get(id=pf)
            a,b = User.objects.get_or_create(email=pb['email'],defaults={'username':pb['email'],'first_name':pb['first_name'],'last_name':pb['last_name'],'gender':pb['gender'],'type':pb['type']})
            k=User.objects.get(id=a.id)
            
            paym=Payments.objects.filter(paid_for=x)
            if paym==None:
                c,d = Payments.objects.get_or_create(payment_type=PaymentType.objects.get(id=data['payment_type']),paid_method=data['paid_method'],paid_by=k,paid_for=x,paid_to=Accountant.objects.get(esp_id=data['paid_to']),paid_amount=data['paid_amount'],date_of_transaction=date.today(),discount_type=data['discount_type'],total_discount_amount=data['total_discount_amount'],discount_description=data['discount_description'],fine_amount=data['fine_amount'],fine_description=data['fine_description'],short_description=data['short_description'],cheque_no=data['cheque_no'],time=datetime.now())
            
                if not d:
                    return Response('some error')
                else:
                    return Response(data,status=status.HTTP_201_CREATED)    
            else:        
                c,d = Payments.objects.get_or_create(payment_type=PaymentType.objects.get(id=data['payment_type']),paid_method=data['paid_method'],paid_by=k,paid_for=x,paid_to=Accountant.objects.get(esp_id=data['paid_to']),paid_amount=data['paid_amount'],date_of_transaction=date.today(),discount_type=data['discount_type'],total_discount_amount=data['total_discount_amount'],discount_description=data['discount_description'],fine_amount=data['fine_amount'],fine_description=data['fine_description'],short_description=data['short_description'],cheque_no=data['cheque_no'],time=datetime.now())


            return Response(data,status=status.HTTP_202_ACCEPTED)
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})


    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'payment_type':obj.payment_type.name,
            'paid_method':obj.paid_method,
            'paid_by':obj.paid_by.first_name+" "+obj.paid_by.last_name,
            'paid_for':obj.paid_for.user.first_name,
            'paid_amount':obj.paid_amount,
            'date_of_transaction':obj.date_of_transaction,
             }
            output.append(temp)
        return Response(output)    
class StudentAcViewSet(viewsets.ModelViewSet):
    queryset=StudentAc.objects.all()
    serializer_class=StudentAcSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            p=Payments.objects.filter(paid_for=Student.objects.get(id=data['student'])).order_by('date_of_transaction')
            _class=SectionStudent.objects.get(student=Student.objects.get(id=data['student'])).section._class
                


            if p==None:    
                return Response('No payments instance for this student found')
            else:
                #pv=p.values()
                #pl=[pay for pay in pv]
                pl=p
                print(pl)
                num=len(pl)
                print(num)
                for i in range(num):
                    if i==0:
                        payment=pl[i]
                        pid=payment.id
                        print(payment)
                        if pid==1:
                            rate=payment.payment_type.rate
                            paid_date=payment.date_of_transaction
                            paid_amount=payment.paid_amount
                            discount_type=payment.discount_type
                            discount_amount=payment.total_discount_amount
                            fine_amount=payment.fine_amount
                            total_due=rate-discount_amount+fine_amount-paid_amount
                            if total_due>0:
                                due_amount=total_due
                                credit_amount=0
                                balance=0+due_amount
                            elif total_due<0:
                                due_amount=0
                                credit_amount=0-total_due
                                balance=0-credit_amount
                            elif total_due==0:
                                due_amount=0
                                credit_amount=0
                                balance=0

                            stac,c=StudentAc.objects.update_or_create(student=Student.objects.get(id=data['student']),payments=payment,due_amount=due_amount,credit_amount=credit_amount,balance=balance)           
                        elif pid>1:
                            rate=payment.payment_type.rate
                            paid_date=payment.date_of_transaction
                            paid_amount=payment.paid_amount
                            discount_type=payment.discount_type
                            discount_amount=payment.total_discount_amount
                            fine_amount=payment.fine_amount
                            total_due=rate-discount_amount+fine_amount-paid_amount                            
                            if total_due>0:
                                due_amount=total_due
                                credit_amount=0
                                balance=0+due_amount
                            elif total_due<0:
                                due_amount=0
                                credit_amount=0-total_due
                                balance=0-credit_amount
                            elif total_due==0:
                                due_amount=0
                                credit_amount=0
                                balance=0
                            try:                                                                
                                stac=StudentAc.objects.get(student=Student.objects.get(id=data['student']))
                            except:
                                stac,c=StudentAc.objects.update_or_create(student=Student.objects.get(id=data['student']),payments=payment,due_amount=due_amount,credit_amount=credit_amount,balance=balance)           


                            stac.payments=payment
                            stac.due_amount=due_amount
                            stac.credit_amount=credit_amount
                            stac.balance=balance
                            stac.save()

                    elif i>0:
                        payment=pl[i]
                        stacc=StudentAc.objects.get(payments=pl[i-1])
                        rate=payment.payment_type.rate
                        paid_date=payment.date_of_transaction
                        paid_amount=payment.paid_amount
                        discount_type=payment.discount_type
                        discount_amount=payment.total_discount_amount
                        fine_amount=payment.fine_amount
                        if payment.payment_type.name==0:
                            no_of_months=(paid_date.month-pl[i-1].date_of_transaction.month)
                            payable_fee=rate*no_of_months
                            total_due=payable_fee-discount_amount+fine_amount+stacc.balance-paid_amount
                            
                            if total_due>0:
                                due_amount=total_due
                                credit_amount=0
                                balance=0+due_amount
                            elif total_due<0:
                                due_amount=0
                                credit_amount=0-total_due
                                balance=0-credit_amount
                            elif total_due==0:
                                due_amount=0
                                credit_amount=0
                                balance=0


                        elif payment.payment_type.name==1:

                            no_of_quarters=(paid_date.month-pl[i-1].paid_date.month)/4
                            payable_fee=rate*no_of_quarters
                            total_due=payable_fee-discount_amount+fine_amount+stacc.balance-paid_amount

                            if total_due>0:
                                due_amount=total_due
                                credit_amount=0
                                balance=0+due_amount
                            elif total_due<0:
                                due_amount=0
                                credit_amount=0-total_due
                                balance=0-credit_amount
                            elif total_due==0:
                                due_amount=0
                                credit_amount=0
                                balance=0


                        elif payment.payment_type.name==2:

                            no_of_years=(paid_date.month-pl[i-1].paid_date.month)/12
                            payable_fee=rate*no_of_years
                            total_due=payable_fee-discount_amount+fine_amount+stacc.balance-paid_amount
                            if total_due>0:
                                due_amount=total_due
                                credit_amount=0
                                balance=0+due_amount
                            elif total_due<0:
                                due_amount=0
                                credit_amount=0-total_due
                                balance=0-credit_amount
                            elif total_due==0:
                                due_amount=0
                                credit_amount=0
                                balance=0
                        elif payment.payment_type.name==4:

                            total_due=rate+stacc.balance-discount_amount+fine_amount-paid_amount

                            if total_due>0:
                                due_amount=total_due
                                credit_amount=0
                                balance=0+due_amount
                            elif total_due<0:
                                due_amount=0
                                credit_amount=0-total_due
                                balance=0-credit_amount
                            elif total_due==0:
                                due_amount=0
                                credit_amount=0
                                balance=0                                
                                
                        stac=StudentAc.objects.get(student=Student.objects.get(id=data['student']))
                        stac.payments=payment
                        stac.due_amount=due_amount
                        stac.credit_amount=credit_amount
                        stac.balance=balance
                        stac.save()
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)   
    def list(self,request):
        objects=StudentAc.objects.all()
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'student':obj.student.user.first_name+" "+obj.student.user.last_name,
            'payment_details':{'due_amount':obj.due_amount,
            'credit_amount':obj.credit_amount,
            'balance':obj.balance,
            'misc_fee_allocated':obj.balance-obj.due_amount}
            }
            output.append(temp)
        return Response(output) 



# class Fee_CategoryViewSet(viewsets.ModelViewSet):
#     serializer_class=FeeCategorySerializer
#     queryset=Fee_Category.objects.all()
#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             a,b=Fee_Category.objects.get_or_create(name=data['name'],description=data['description'])
#             if not b:
#                 return Response('Category already exists',status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)
# class Fee_AllocationViewSet(viewsets.ModelViewSet):
#     serializer_class=FeeAllocationSerializer
#     queryset=Fee_Allocation.objects.all()

#     def create(self,request):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             if data['_class']==None:
#                 for cl in Class.objects.all():
#                     a,b=Fee_Allocation.objects.get_or_create(fee_category=Fee_Category.objects.get(id=data['fee_category']),_class=Class.objects.get(id=cl.id),amount=data['amount'])
#                     if not b:
#                         return Response({"Error":"Fee allocation instance already exists"},status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         sl=Section.objects.filter(_class=cl)
#                         # slv=sl.values()
#                         # slvl=[val for val in slv]
#                         for obj in sl:
#                             scstd=SectionStudent.objects.filter(section=obj)
#                             for scs in scstd:
#                                 std=scs.student
#                                 try:
#                                     stdac=StudentAc.objects.get(student=std)
#                                 except:
#                                     return Response('Cannot assign amount to student account because student account does not exist')
#                                 newbal=stdac.balance+a.amount
#                                 stdac.balance=newbal
#                                 stdac.save()    


#                         continue
#             elif data['_class']:
#                 a,b=Fee_Allocation.objects.get_or_create(fee_category=Fee_Category.objects.get(id=data['fee_category']),_class=Class.objects.get(id=data['_class']),amount=data['amount'])
#                 if not b:
#                     return Response({"Error":"Fee allocation instance already exists"},status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     sl=Section.objects.filter(_class=Class.objects.get(id=data['_class']))
#                         # slv=sl.values()
#                         # slvl=[val for val in slv]
#                     for obj in sl:
#                         scstd=SectionStudent.objects.filter(section=obj)
#                         for scs in scstd:
#                             std=scs.student
#                             try:
#                                 stdac=StudentAc.objects.get(student=std)
#                             except:
#                                 return Response('Cannot assign amount to student account because student account does not exist')
#                             newbal=stdac.balance+a.amount
                            
#                             stdac.balance=newbal
#                             stdac.save()
#                         continue                           
#             return Response(data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)        
                  
#     def retrieve(self,request,pk):
#         try:
#             obj=Fee_Allocation.objects.get(id=pk)
#         except:
#             return Response({"Error":"Fee allocation object not found"},status=status.HTTP_404_NOT_FOUND)
#         temp={"fee_category":obj.fee_category.name,
#         "class":obj._class.name,
#         "amount":obj.amount}
#         return Response(temp)
#     def update(self,request,pk):
#         try:
#             obj=Fee_Allocation.objects.get(id=pk)
#         except:
#             return Response({"Error":"Fee allocation object not found"},status=status.HTTP_404_NOT_FOUND)
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             data=serializer.data
#             if data['_class']==None:
#                 for cl in Class.objects.all():
#                     obj.fee_category=Fee_Category.objects.get(id=data['fee_category'])
#                     obj._class=Class.objects.get(id=cl.id)
#                     obj.amount=data['amount']
#                     obj.save()
#             return Response(data,status=status.HTTP_200_OK)
#         else:
#             return Response({"Detail":[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

        
class TeacherSalaryViewset(viewsets.ModelViewSet):
    queryset=TeacherSalary.objects.all()
    serializer_class=TeacherSalarySerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        try:
            request.data['year']<=(date.today()).year
        except:
            return Response({'error':['the year value is invalid']} )
        try:
            request.data['month'] in range (1,13)
        except:
            return Response({'error':['month value is not valid']})    

        try:
            t=Teacher.objects.get(id=request.data['teacher'])
        except:
            return Response({'sorry':'Teacher does not exist,please create the related teacher object first'},status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            data=serializer.data

            
            
            ts,b=Teacher.objects.get_or_create(teacher=t,defaults={'year':data['year'],'month':data['month']},salary=data['salary'],deduction=data['deduction'])
            if not b:
                return Response({'Error':['The teacher salary object already exists']},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)        

    def list(self,request):
        objects=self.queryset
        output=[]
        
        for obj in objects:

            temp={'id':obj.id,
            'teacher':obj.teacher.user.first_name+" "+obj.teacher.user.last_name,
            'year':str(obj.year)+" "+"A.D.",
            'month':calendar.month_name[obj.month],
            'deduction':obj.deduction
            }
            output.append(temp)
        return Response(output)
    def retrieve(self,request,pk):
        try:
            obj=TeacherSalary.objects.get(id=pk)
        except:
            return Response({'error':['teacher salary not found']},status=status.HTTP_404_NOT_FOUND)
        temp={'id':obj.id,
        'teacher':obj.teacher.user.first_name+" "+obj.teacher.user.last_name,
        'year':str(obj.year)+" "+"A.D.",
        'month':calendar.month_name[obj.month],
        'deduction':obj.deduction
        }

        return Response(temp)
    def update(self,request,pk):
        try:
            ts=TeacherSalary.objects.get(id=pk)
        except:
            return Response({'error':['Teacher Salary object not found']},status=status.HTTP_404_NOT_FOUND)
        serializer=TeacherSalaryUpdateSerializer()
        if serializer.is_valid():
            data=serializer.data
            ts.teacher=Teacher.objects.get(id=data['teacher'])
            ts.salary=data['salary']
            ts.deduction=data['deduction']
            ts.save()
        return Response(data,status=status.HTTP_200_OK)    


