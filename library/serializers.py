from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from main.models import User,USER_TYPE
from main.helpers.tuple import get_choice_string
from library.models import *

class BookCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    code = serializers.CharField()

    class Meta:
        model = BookCategory
        fields = ('id', 'name', 'code', )

class BookSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    isbn=serializers.CharField(validators=[UniqueValidator(queryset=Book.objects.all(), message="Book with ISBN already exists")])
    category=serializers.PrimaryKeyRelatedField(queryset=BookCategory.objects.all())
    # condition=serializers.ChoiceField(choices=book_condition_c)
    
    # def get_book_condition(self, obj):
    #     return get_choice_string(book_condition_c,obj.book_condition)

    class Meta:
        model = Book
        #fields = ('__all__')
        exclude = ('date_deleted', )
        #extra_kwargs = {"isbn": {"error_messages": {"unique": "Book with ISBN already exists"}}}


class BookIssueSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    book=serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    date_issue=serializers.DateField()
    date_due=serializers.DateField(required=False)


    def validate(self, data):
        """
        Check that the book is available
        """
        data['date_due'] = get_due_date(data['date_issue'])
        bi = BookIssue.objects.filter(book=data['book'], status=1).count()
        if bi >= data['book'].no_of_copies:
            raise serializers.ValidationError({'Detail':'Book is not available'})
        return data


    class Meta:
        model = BookIssue
        exclude = ('date_deleted',  )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class BookIssueGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    book = BookSerializer()
    date_issue = serializers.DateTimeField()
    date_due = serializers.DateTimeField()
    date_returned = serializers.DateTimeField()
    status = serializers.CharField()
    class Meta:
        fields = ('id', 'user', 'book', 'date_issue', 'date_due', 'date_returned', 'status')
