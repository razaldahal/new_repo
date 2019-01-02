from rest_framework import serializers
from .models import *
from main.models import User,USER_TYPE

from main.helpers.tuple import get_choice_string

class CategorySerializer(serializers.Serializer):
    name=serializers.CharField()
    section_code=serializers.SlugField()

class BooksSerilaizer(serializers.Serializer):
    purchase_date=serializers.DateField()
    bill_no=serializers.CharField()
    isbn_no=serializers.SlugField()
    no=serializers.CharField()
    title=serializers.CharField()
    author=serializers.CharField()
    edition=serializers.CharField()
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    publisher=serializers.CharField()
    no_of_copies=serializers.IntegerField()
    shelf_no=serializers.CharField()
    position=serializers.CharField()
    book_cost=serializers.IntegerField()
    book_condition_c=(
    (1,'AS NEW'),
    (2,'FINE'),
    (3,'VERY GOOD'),
    (4,'GOOD'),
    (5,'FAIR'),
    (6,'POOR'),
    (7,'LOST'),
    (8,'MISSING')
    )
    book_condition=serializers.ChoiceField(choices=book_condition_c)
    def get_book_condition(self, obj):
        return get_choice_string(book_condition_c,obj.book_condition)
class Issue_bookSerilaizer(serializers.Serializer):
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_type=serializers.ChoiceField(choices=USER_TYPE)
    book=serializers.PrimaryKeyRelatedField(queryset=Books.objects.all())
    issue_date=serializers.DateField()
    due_date=serializers.DateField() 
class Request_bookSerializer(serializers.Serializer):
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_type=serializers.ChoiceField(choices=USER_TYPE)
    book=serializers.PrimaryKeyRelatedField(queryset=Books.objects.all())
    request_date=serializers.DateField()
    status=serializers.CharField(max_length=10)
    accept=serializers.BooleanField()        
class Book_returnSerializer(serializers.Serializer):
    book=serializers.PrimaryKeyRelatedField(queryset=Issue_book.objects.all())
    returned_date=serializers.DateField()
    fine_amount=serializers.IntegerField()
    remarks=serializers.CharField()