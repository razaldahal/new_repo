from rest_framework import serializers
from .models import *
from main.models import User,USER_TYPE



class CategorySerializer(serializers.Serializer):
    name=serializers.CharField()
    section_code=serializers.SlugField()

class BooksSerilaizer(serializers.Serializer):
    purchase_date=serializers.DateField()
    bill_no=serializers.CharField()
    isbn_no=serializers.SlugField()
    no=serializers.CharField(max_length=20)
    title=serializers.CharField(max_length=30)
    author=serializers.CharField(max_length=30)
    edition=serializers.CharField(max_length=20)
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    publisher=serializers.CharField(max_length=30)
    no_of_copies=serializers.IntegerField()
    shelf_no=serializers.CharField(max_length=20)
    position=serializers.CharField(max_length=20)
    book_cost=serializers.IntegerField()
    book_condition=(
    ('As_new','AS NEW'),
    ('fine','FINE'),
    ('verygood','VERY GOOD'),
    ('good','GOOD'),
    ('fair','FAIR'),
    ('poor','POOR'),
    ('lost','LOST'),
    ('missing','MISSING')
    )
    book_condition=serializers.ChoiceField(choices=book_condition)
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