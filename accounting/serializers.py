from rest_framework import serializers
from .models import *

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ('id','name','description')

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
    remarks = serializers.CharField()

