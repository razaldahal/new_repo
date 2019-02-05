from datetime import datetime, timedelta
from django.db import models
from main.models import BaseModel, User, USER_TYPE

DUE_DAY_LIMIT = 14

book_condition_c = (
    (1,'NEW'),
    (2,'FINE'),
    (3,'VERY GOOD'),
    (4,'GOOD'),
    (5,'FAIR'),
    (6,'POOR'),
    (7,'LOST'),
    (8,'MISSING')
    )

issue_status_c = (
    (1, 'ISSUED'),
    (2, 'RETURNED'),

    )

def get_due_date(d):
    return d + timedelta(days=DUE_DAY_LIMIT)

class BookCategory(BaseModel):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30)

    class Meta:
        db_table = 'library_book_category'
        verbose_name_plural = 'BookCategory'

    def __str__(self):
        return self.name


class Book(BaseModel):
    purchase_date = models.DateField(null=True, blank=True)
    bill_no = models.CharField(max_length=20, null=True)
    isbn = models.CharField(max_length=20, unique=True)
    number = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30, null=True)
    edition = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(BookCategory,on_delete=models.CASCADE)
    publisher = models.CharField(max_length=30, null=True)
    no_of_copies = models.IntegerField()
    shelf_no = models.CharField(max_length=20,null=True )
    position = models.CharField(max_length=20, null=True )
    cost = models.FloatField()
    condition = models.IntegerField(choices=book_condition_c)

    class Meta:
        db_table = 'library_book'
        verbose_name_plural = 'Book'

    def __str__(self):
        return self.title


class BookIssue(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    date_issue = models.DateTimeField()
    date_due = models.DateTimeField()

    status = models.IntegerField(choices=issue_status_c, default=1)

    date_returned = models.DateTimeField(null=True, blank=True)
    fine_amount = models.FloatField(default=0)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'library_book_issue'
        verbose_name_plural = 'BookIssue'