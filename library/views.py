from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework import filters,generics
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import *
from .serializers import *



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    http_method_names = ['post', 'get', 'delete']

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            category, c = BookCategory.objects.get_or_create(name=data['name'],code=data['code'])
            if not c:
                return Response({'Detail':'Category already Exists!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)       



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookSearchViewSet(APIView):

    def search(self):
        output = []
        q = self.request.GET.get('q',False)
        if q:

            filter_params = {
                'title__icontains':q,
                
            }
            print(filter_params)
            books = []
            objects = Book.objects.filter(**filter_params)
            for obj in objects:
                books.append(obj)

            books = BookSerializer(books, many=True)
            output = books.data
        return output

    @swagger_auto_schema(manual_parameters=[
        
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ])
    def get(self, request, format=None):
        """
        Book search
        """
        output = self.search()
        return Response(output)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.filter().order_by('date_due')
    serializer_class = BookIssueSerializer
    http_method_names = ['post', 'get']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return BookIssueGetSerializer
        return BookIssueSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(status=1)
        output = []
        for q in queryset:
            tmp = {
                'id': q.id,
                'user': q.user,
                'book': q.book,
                'date_issue': datetime.strftime(q.date_issue, '%Y-%m-%d %I:%M'),
                'date_due': datetime.strftime(q.date_due, '%Y-%m-%d %I:%M'),
                'status': q.status,
                'date_returned': q.date_returned
            }
            tmp = self.get_serializer(tmp).data
            output.append(tmp)
        return Response(output)

class ReturnViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.filter().order_by('-date_created')
    serializer_class = BookIssueSerializer
    http_method_names = ['get']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return BookIssueGetSerializer
        return BookIssueSerializer

    def retrieve(self, request, pk):
        status = int(request.GET.get('mode', 2)) # 2 is returned, 1 is renewed.
        bi = self.get_object()
        bi.status = status

        if status == 1:
            bi.date_issue = datetime.now()
            bi.date_due = get_due_date(bi.date_issue)
        else:
            bi.date_returned = datetime.now()
        bi.save()
        return Response({'id': bi.id})
