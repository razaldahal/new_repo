from rest_framework import serializers
from admission.serializers import UserSerializer
from .models import Payments,Studentpayments,Accountant
from student.models import Student
from teacher.models import Teacher
class AccountantSerializer(serializers.Serializer):
    user= UserSerializer()
    esp_id= serializers.SlugField()

class PaymentsSerializer(serializers.Serializer):
    payment_type=serializers.IntegerField()
    paid_method=serializers.IntegerField()
    paid_by=UserSerializer()
    paid_for=serializers.IntegerField()
    paid_to=serializers.PrimaryKeyRelatedField(queryset=Accountant.objects.all())
    paid_amount=serializers.IntegerField()
    date_of_transaction=serializers.DateField()
    short_description=serializers.CharField()
    cheque_no=serializers.CharField(required=False)
class StudentpaymentsSerializer(serializers.Serializer):
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    payment=serializers.PrimaryKeyRelatedField(queryset=Payments.objects.all())

class FeesDueSerializer(serializers.Serializer):
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    fee_type=serializers.IntegerField()
    ac_start_date=serializers.DateField()
    rate=serializers.IntegerField() 
    date=serializers.DateField()

class TeacherSalarySerializer(serializers.Serializer):
    teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    year=serializers.IntegerField()
    month=serializers.IntegerField()
    salary=serializers.IntegerField()
    deduction=serializers.IntegerField()    


class TeacherSalaryUpdateSerializer(serializers.Serializer):
    salary=serializers.IntegerField()
    deduction=serializers.IntegerField()
    teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())    
    