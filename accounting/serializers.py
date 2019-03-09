from django.db.models import Sum

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from academic.serializers import FacultySerializer
from .models import *

from datetime import datetime, timedelta, time


def getTodayCollection():
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    rows = StudentPayment.objects.filter(date_created__lt=today_end, date_created__gt=today_start)
    total = 0
    for row in rows:
        if row.payment_type == 2:
            total += row.amount
    return total

def getTotalDue():
    # total_amount = StudentPayment.objects.aggregate(Sum('amount'))['amount__sum']
    # total_paid = StudentPayment.objects.filter(payment_type=1).aggregate(Sum('amount'))['amount__sum']
    # print(total_amount, total_paid)
    # return total_amount - total_paid
    payments = StudentPayment.objects.filter()
    current_due = 0
    for p in payments:
        if p.payment_type == 1:
            current_due += p.amount
            
        else:
            current_due -= p.amount
    return current_due



class FacultySalaryGetSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    class Meta:
        model = FacultySalary
        fields = ('__all__')

class FacultyPostSerializer(serializers.ModelSerializer):
    faculty_id = serializers.IntegerField()
    class Meta:
        model = FacultySalary
        fields = (
            'id','faculty_id','salary','remarks',
            )
        validators = [
            UniqueTogetherValidator(
                queryset=FacultySalary.objects.all(),
                fields=('faculty_id',)
            )
        ]
class FacultySalaryUpdateSerializer(serializers.ModelSerializer):
    faculty_id = serializers.IntegerField()
    class Meta:
        model = FacultySalary
        fields = ('faculty_id','salary')
    
class FacultySalaryPaymentGetSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    class Meta:
        model = FacultySalaryPayment
        fields = ('__all__')

class FacultySalaryPaymentSerializer(serializers.ModelSerializer):
    faculty_id = serializers.IntegerField()
    class Meta:
        model = FacultySalaryPayment
        fields = ('faculty_id','month','amount','remarks')



class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ('id','name','description')


class ExpenseGetSerializer(serializers.ModelSerializer):
    expense_type = serializers.CharField(source='expense_type.name')
    class Meta:
        model = DailyExpense
        fields = ('id', 'expense_type', 'receipt_number', 'expense_detail', 'amount', 'expense_date',)

class DailyExpenseSerializer(serializers.ModelSerializer):
    expense_type = serializers.IntegerField()
    class Meta:
        model = DailyExpense
        fields = ('id','expense_type','expense_detail','amount','expense_date','receipt_number')

class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = ('id','name','description')

class FeeAllocationSerializer(serializers.Serializer):
    fee_for = serializers.IntegerField()
    _class = serializers.IntegerField(required=False)
    fee_category = serializers.IntegerField()
    total_amount = serializers.IntegerField()



class FeeAllocationGetSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='_class.course.name')
    _class = serializers.CharField(source='_class.name')
    fee_category = serializers.CharField(source='fee_category.name')
    total_amount = serializers.FloatField()

    class Meta:
        model = FeeAllocation
        fields = ('id', 'course', '_class', 'fee_category', 'total_amount', )

class FeeAllocationUpdateSerializer(serializers.Serializer):
    total_amount = serializers.IntegerField()

class FeeCollectionSerializer(serializers.Serializer):
    payment_detail = serializers.ListField()
    student_id = serializers.IntegerField()
    mode_of_payment = serializers.IntegerField(required=False,default=1)
    receipt_number = serializers.IntegerField(required=False)
    remarks = serializers.CharField(required=False)


class StudentPaymentSerializer(serializers.Serializer):
    fee_allocation_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    student_id = serializers.IntegerField()
    remarks = serializers.CharField(required=False)
    payment_type = serializers.IntegerField()

