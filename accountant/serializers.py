from rest_framework import serializers
from admission.serializers import UserSerializer
from .models import Payments,Accountant,payment_type_c,PaymentType,get_choice_string,Class,discount_type_c,Fee_Allocation,Fee_Category
from student.models import Student
from teacher.models import Teacher
class AccountantSerializer(serializers.Serializer):
    user= UserSerializer()
    esp_id= serializers.SlugField()

class PaymentTypeSerializer(serializers.Serializer):
    _class=serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    name=serializers.ChoiceField(choices=payment_type_c)
    rate=serializers.IntegerField()
    def get_name(self,obj):
        return get_choice_string(payment_type_c,obj.name)
class PaymentsSerializer(serializers.Serializer):
    payment_type=serializers.PrimaryKeyRelatedField(queryset=PaymentType.objects.all())
    paid_method=serializers.IntegerField()
    paid_by=UserSerializer()
    paid_for=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    paid_to=serializers.PrimaryKeyRelatedField(queryset=Accountant.objects.all())
    paid_amount=serializers.IntegerField()
    short_description=serializers.CharField()
    cheque_no=serializers.CharField(required=False)
    discount_type=serializers.ChoiceField(choices=discount_type_c)
    total_discount_amount=serializers.IntegerField(required=False)
    discount_description=serializers.CharField()
    fine_amount=serializers.IntegerField()
    fine_description=serializers.CharField()
class FeeCategorySerializer(serializers.Serializer):
    name=serializers.CharField()
    description=serializers.CharField()

class FeeAllocationSerializer(serializers.Serializer):
    fee_category=serializers.PrimaryKeyRelatedField(queryset=Fee_Category.objects.all())
    _class=serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(),required=False)
    amount=serializers.IntegerField()

class StudentAcSerializer(serializers.Serializer):
    student=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    



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
    