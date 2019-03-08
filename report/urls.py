from django.urls import path,include
from django.conf.urls import url
from django.conf.urls import url
from rest_framework import routers
from rest_framework_nested import routers

from .views import *

router = routers.SimpleRouter()

router.register(r'student', StudentFilterViewSet)
router.register(r'library', LibraryReportViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),

]