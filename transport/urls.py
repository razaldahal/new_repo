from django.urls import path,include
from django.conf.urls import url
from django.conf.urls import url
from rest_framework import routers
from rest_framework_nested import routers


from .views import *

router = routers.SimpleRouter()

#router.register(r'category', CategoryViewSet)

urlpatterns = [

	# url(r'search', BookSearchViewSet.as_view(), name='book-search'),
	# url(r'^', include(router.urls)),

]