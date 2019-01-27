from django.urls import path,include
from rest_framework import routers
from .views import ReportViewset
from django.conf.urls import url


router = routers.SimpleRouter()
urlpatterns=[
    url('',ReportViewset.as_view({'get':'list'})),
	path('',include(router.urls)),
]