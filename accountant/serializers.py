from rest_framework import serializers
from admission.serializers import UserSerializer
from .models import Payments,Payment_posting_reference,Ledger,Studentpayments,Accountant
from student.models import Student
class AccountantSerializer(serializers.Serializer):
    user= UserSerializer()
    esp_id= serializers.SlugField()

class PaymentsSerializer(serializers.Serializer):
    payment_type=serializers.IntegerField()
    paid_method=serializers.IntegerField()
    paid_by=UserSerializer()
    paid_for=serializers.IntegerField()
    paid_to=AccountantSerializer()
    paid_amount=serializers.IntegerField()
    date_time_of_transaction=serializers.DateTimeField()
    short_description=serializers.CharField()
    cheque_no=serializers.CharField(required=False)
class Payment_posting_referenceSerilaizer(serializers.Serializer):
    payment_details=PaymentsSerializer()
    balance=serializers.IntegerField() 
class LedgerSerailizer(serializers.Serializer):
    payment_posting_reference=Payment_posting_referenceSerilaizer()
    description=serializers.CharField()
class StudentpaymentsSerializer(serializers.Serializer):
    student=UserSerializer()
    payment=PaymentsSerializer()
    ledger=LedgerSerailizer() 
class FeesDueSerializer(serializers.Serializer):
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    fee_type=serializers.IntegerField()
    ac_start_date=serializers.DateField()
    rate=serializers.IntegerField() 
    date=serializers.DateField()