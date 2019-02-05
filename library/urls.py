from django.urls import path,include
from django.conf.urls import url
from django.conf.urls import url
from rest_framework import routers
from rest_framework_nested import routers


from .views import *

router = routers.SimpleRouter()

router.register(r'category', CategoryViewSet)
router.register(r'book', BookViewSet)

router.register(r'issue', IssueViewSet)
router.register(r'return', ReturnViewSet)

urlpatterns = [

	url(r'search', BookSearchViewSet.as_view(), name='book-search'),
	url(r'^', include(router.urls)),

]