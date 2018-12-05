from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.response import Response
# Create your views here.


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
                x = User.objects.get(email=user['email'])
                y = Accountant.objects.get_or_create(user=x,esp_id=esp_idd)
        
            except:
                a,b = User.objects.get_or_create(email=user['email'],defaults={'first_name':user['first_name'],'last_name':user['last_name'],'username':user['email'],'gender':user['gender'],'type':user['type']}) 
    
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
            c,d = Payments.objects.get_or_create(payment_type=data['payment_type'],paid_method=data['paid_method'],paid_by=k,paid_for=x,paid_to=Accountant.objects.get_or_create(data['paid_to'])[0],paid_amount=data['paid_amount'],date_time_of_transaction=data['date_time_of_transaction'],short_description=data['short_description'],cheque_no=data['cheque_no'])
            e,f = Payment_posting_reference.objects.get_or_create(payment_details=c,balance=0-c.paid_amount)
            g,h = Ledger.objects.get_or_create(payment_posting_reference=e,description=c.short_description)
            i,j = Studentpayments.objects.get_or_create(student=c.paid_for,payments=c,ledger=g)
            if not j:
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
            'date_time_of_transaction':obj.date_time_of_transaction,
             }
            output.append(temp)
        return Response(output)    

class Payment_posting_referenceViewsets(viewsets.ModelViewSet):
    queryset=Payment_posting_reference.objects.all()
    serializer_class=Payment_posting_referenceSerilaizer

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'payment_details':obj.payment_details.paid_for.user.first_name,
            'balance':obj.balance}
            output.append(temp)
        return Response(output) 
class FeesdueViewSets(viewsets.ModelViewSet):
    queryset=Fees_due.objects.all()
    serializer_class=FeesDueSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a = Student.objects.get(id=data['student'])
            Fees_due.objects.get_or_create(date=data['date'],student_id=a.id,fee_type=data['fee_type'],ac_start_date=data['ac_start_date'],rate=data['rate'])
            if data['fee_type']==0:
                b=Payments.objects.filter(paid_for_id=a.id).order_by('-date_time_of_transaction')
                d=b[0]
                c=Payment_posting_reference.objects.get_or_create(payment_details=d,balance=data['rate']*(int((data['date']-d.date_time_of_transaction.date).days)/30)+balance)
                return Response({c})    

            elif data['fee_type']==1:
                b=Payments.objects.filter(paid_for_id=a.id).order_by('-date_time_of_transaction')
                d=b[0]
                c=Payment_posting_reference.objects.get_or_create(payment_details=d,balance=data['rate']*(int((data['date']-d.date_time_of_transaction.date).days)/120)+balance)
                return Response({c})    

            elif data['fee_type']==2:
                b=Payments.objects.filter(paid_for_id=a.id).order_by('-date_time_of_transaction')
                d=b[0]
                c=Payment_posting_reference.objects.get_or_create(payment_details=d,balance=data['rate']*(int((data['date']-d.date_time_of_transaction.date).days)/360)+balance)
                return Response({c})    





        

        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})