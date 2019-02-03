from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.response import Response
# Create your views here.
from datetime import datetime,date
import calendar
from teacher.models import Teacher
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
            c,d = Payments.objects.get_or_create(payment_type=PaymentType.objects.get(id=data['payment_type']),paid_method=data['paid_method'],paid_by=k,paid_for=x,paid_to=Accountant.objects.get(esp_id=data['paid_to']),paid_amount=data['paid_amount'],date_of_transaction=date.today(),discount_type=data['discount_typr'],total_discount_amount=data['total_discount_amount'],discount_description=data['discount_description'],fine_amount=data['fine_amount'],fine_description=data['fine_description'],short_description=data['short_description'],cheque_no=data['cheque_no'])
            
            if not d:
                return Response('some error')
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})


    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'payment_type':obj.payment_type,
            'paid_method':obj.paid_method,
            'paid_by':obj.paid_by.first_name+" "+obj.paid_by.last_name,
            'paid_for':obj.paid_for.user.first_name,
            'paid_amount':obj.paid_amount,
            'date_of_transaction':obj.date_of_transaction,
             }
            output.append(temp)
        return Response(output)    
class StudentAcViewSet(viewsets.ViewSet):
    queryset=StudentAc.objects.all()
    serializer_class=StudentAcSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=request.data
            p=Payments.objects.filter(paid_for=Student.objects.get(id=data['student']))
            if p==None:    
                return Response('No payments instance for this student found')
            else:
                pv=p.values()
                pl=[pay for pay in pv]
                num=pl.count
                for i in range(num):
                    if i==0:
                        payment=pl[i]
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
                            balance=0+due_amount
                        elif total_due==0:
                            due_amount=0
                            credit_amount=0
                            balance=0

                        stac,c=StudentAc.objects.get_or_create(student=Student.objects.get(id=data['student']),payments=payment,due_amount=due_amount,credit_amount=credit_amount,balance=balance)           

                    elif i>0:
                        payment=pl[i]
                        stacc=StudentAc.objects.get(payments=pl[i-1])
                        rate=payment.rate
                        paid_date=payment.paid_date
                        paid_amount=payment.paid_amount
                        discount_type=payment.discount_type
                        discount_amount=payment.discount_amount
                        fine_amount=payment.fine_amount
                        if payment.payment_type.name==0:
                            no_of_months=(paid_date-pl[i-1].paid_date).month
                            payable_fee=rate*no_of_months
                            total_due=payable_fee-discount_amount+fine_amount+stacc.balance
                            
                            if total_due>0:
                                due_amount=total_due
                                credit_amount=0
                                balance=0+due_amount
                            elif total_due<0:
                                due_amount=0
                                credit_amount=0-total_due
                                balance=0+due_amount
                            elif total_due==0:
                                due_amount=0
                                credit_amount=0
                                balance=0

                            stac,c=StudentAc.objects.get_or_create(student=Student.objects.get(id=data['student']),payments=payment,due_amount=due_amount,credit_amount=credit_amount,balance=balance)           

                        elif payment.payment_type.name==1:

                            no_of_quarters=((paid_date-pl[i-1].paid_date).month)/4
                            payable_fee=rate*no_of_months
                            total_due=payable_fee-discount_amount+fine_amount+stacc.balance



    


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


